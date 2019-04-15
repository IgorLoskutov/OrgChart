# -*- coding: utf-8 -*-
from flask import render_template, request
from app import app, db
from app.models import Employee

from sqlalchemy import func

import math


@app.route('/')
@app.route('/index')
def index():
    # user = {'username': 'Sieger'}
    e = Employee().query.get(0)
    template = 'index.html'

    def get_subords(i):
        subords = Employee().query.filter(Employee.manager_id==i).all()
        return subords

    if 'emp_id' in request.args:
        try:
            emp_id = int(request.args['emp_id'])
        except ValueError:
            pass
        e = Employee().query.get(emp_id)
        template = 'subords.html'
        print(request.args)

    return render_template(
        template,
        e=e,
        Employee=Employee,
        get_subords=get_subords
        )

@app.route('/table', methods = ['POST', 'GET'])
def table():
    template = 'table.html'
    sort_key = 'full_name' #default sort column if not set in request
    limit = 10 #default limit if not set in request
    offset = 0 #default offset
    page_n = 5
    current_page = 1

    sort_keys={     #not keeping Employee fields names on front
        'id':'id',
        'Manager id':'manager_id',
        'Name':'full_name',
        'Position':'position',
        'Employed':'work_start',
        'Salary':'salary'
        }

    if request.args:
        if 'limit' in request.args:
            limit = int(request.args['limit'])
        if 'sort' in request.args:
            sort_key=sort_keys[request.args['sort']]
        if 'page' in request.args:
            try:
                current_page = int(request.args['page'])
                offset = (current_page - 1) * limit #pagination of the output
                page_n = limit
            except ValueError:
                pass
        limit += offset
        template = 'rows.html'

    if request.args and 'find' in request.args and request.args['find']!= '':
        '''search 'find' input through all VARCHAR, INT, NUM fields
        whatever column names are'''
        find_str = "%{}%".format(request.args['find'])
        find = request.args['find']
        emps = Employee.query.limit(0) #empty query to "append" UNION SELECT
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
                            Employee.__dict__[c.name]==find
                            )
                        )
                except :
                    pass
    else:
        emps = Employee().query

    pages = math.ceil(emps.count()/page_n)

    if pages <= 8:
        pages = (1, pages)
    elif current_page>=pages-3:
        pages = (pages-7, pages)
    else:
        pages = (current_page-3, max(current_page+4, 8))

    emps = emps.order_by(Employee.__dict__[sort_key])[offset:limit]

    return render_template(
        template,
        emps = emps,
        page = pages
        )