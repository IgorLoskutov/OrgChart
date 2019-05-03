# -*- coding: utf-8 -*-
from math import ceil
from decimal import Decimal

from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required

from werkzeug.urls import url_parse
from werkzeug import secure_filename

from app import app, db
from app.models import Employee, Users
from app.forms import LoginForm, NewEmployee


@app.route('/')
@app.route('/index', methods=['POST', 'GET'])
@login_required
def index():
    emp = Employee().query.get(0)
    template = 'index.html'

    def get_subords(i):
        subords = Employee().query.filter(Employee.manager_id == i).all()
        return subords

    if request.method == 'GET':
        if 'emp_id' in request.args:
            try:
                emp_id = int(request.args['emp_id'])
            except ValueError:
                pass
            emp = Employee().query.get(emp_id)
            template = 'subords.html'
    if request.method=='POST':
        '''drag'n'drop changing manager directly in org-tree'''
        employee_id = int(request.form['set_manager_id[employee]'])
        new_manager = int(request.form['set_manager_id[manager]'])
        if employee_id != new_manager:
            empl = Employee().query.get(employee_id)
            empl.manager_id = new_manager
            db.session.add(empl)
            db.session.commit()

    return render_template(
        template,
        e=emp,
        Employee=Employee,
        get_subords=get_subords
        )


@app.route('/table', methods=['POST', 'GET'])
@login_required
def table():
    template = 'table.html'
    sort_key = 'full_name'     # default sort column if not set in request
    limit = 10    # default limit if not set in request
    offset = 0    # default offset
    page_n = 5
    current_page = 1
    sort_keys={     # not keeping Employee fields names on front
        'id': 'id',
        'ManagerID': 'manager_id',
        'Name': 'full_name',
        'Position': 'position',
        'Employed': 'work_start',
        'Salary': 'salary'
        }
    if request.method == 'GET':
        if request.args:
            if 'limit' in request.args:
                limit = int(request.args['limit'])
            if 'sort' in request.args:
                sort_key = sort_keys[request.args['sort']]
            if 'page' in request.args:
                try:
                    current_page = int(request.args['page'])
                    offset = (current_page - 1) * limit    # pagination
                    page_n = limit
                except ValueError:
                    pass
            limit += offset
            template = 'rows.html'
        if 'find' in request.args and request.args['find'] != '':
            '''search 'find' input through all VARCHAR, INT, DEC fields
            whatever column names are'''
            find_str = "%{}%".format(request.args['find'])
            find = request.args['find']
            emps = Employee.query.limit(0)    # empty query to append UNION SELECT
            for c in Employee.__table__.c:
                if 'VARCHAR' in str(c.type):
                    emps = emps.union(
                        Employee.query.filter(
                            Employee.__dict__[c.name].like(find_str)
                            )
                        )
                elif 'INT' in str(c.type) or 'NUM' in str(c.type):
                    try:
                        find = int(find)
                        emps = emps.union(
                            Employee.query.filter(
                                Employee.__dict__[c.name] == find
                                )
                            )
                    except ValueError:
                        pass
        else:
            emps = Employee().query
        pages = ceil(emps.count()/page_n)
        if pages <= 8:
            pages = (1, pages)
        elif current_page >= pages-3:
            pages = (pages-7, pages)
        else:
            pages = (current_page-3, max(current_page+4, 8))
        emps = emps.order_by(Employee.__dict__[sort_key])[offset:limit]
        return render_template(
            template,
            emps=emps,
            page=pages
            )

    if request.method == 'POST':
        '''update employee data from table'''
        if 'update' in request.form:
            field = sort_keys[request.form['field']]
            emp_id = request.form['id']
            update = request.form['update']
            emp = Employee.query.get(emp_id)
            if field == 'full_name':
                emp.full_name = update
            if field == 'position':
                emp.position = update
            if field == 'salary':
                try:
                    emp.salary = Decimal(update)
                except ValueError:
                    pass
            if field == 'manager_id':
                try:
                    if emp.id != int(update):
                        emp.manager_id = int(update)
                except ValueError:
                    pass
            db.session.add(emp)
            db.session.commit()
        if 'fire' in request.form:
            '''fire employee'''
            fire = request.form['fire']
            for sub in Employee.query.filter(Employee.manager_id == fire):
                sub.manager_id = Employee.query.get(fire).manager_id
                db.session.add(sub)
            db.session.delete(Employee.query.get(fire))
            db.session.commit()
        return '', 204


@app.route('/new', methods=['GET', 'POST'])
@login_required
def add_new():
    print("/new")
    form = NewEmployee()
    if form.validate_on_submit():
        filename = None
        if form.pic.data:
            filename = str(form.id.data) + secure_filename(form.pic.data.filename)
            form.pic.data.save('app/static/images'+filename)
        emp = Employee(
                id=form.id.data,
                full_name=form.name.data,
                work_start=form.work_start.data,
                salary=Decimal(form.salary.data),
                position=form.position.data,
                manager_id=form.manager_id.data,
                pic=filename
                )
        db.session.add(emp)
        db.session.commit()

        return redirect(url_for('table'))
    return render_template('newbe.html', title='New Employee', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('table'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
