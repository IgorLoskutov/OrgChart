# -*- coding: utf-8 -*-
from flask import render_template, request
from app import app, db
from app.models import Employee


@app.route('/')
@app.route('/index')
def index():
    # user = {'username': 'Sieger'}
    e = Employee().query.get(0)
    template = 'index.html'

    def get_subords(i):
        subords = Employee().query.filter(Employee.manager_id==i).all()
        return subords


    if request.args:
        e = Employee().query.get(int(request.args['emp_id']))
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
    limit = 25 #default limit if not set in request
    offset = 0 #default offset if not set in request

    sort_keys={
        'id':'id',
        'Manager id':'manager_id',
        'Name':'full_name',
        'Position':'position',
        'Employed':'work_start',
        'Salary':'salary'
        }

    if request.args:
        #offset = request.args['offset'] #pagination of the output
        sort_key=sort_keys[request.args['sort']]
        limit = offset+int(request.args['limit'])
        template = 'rows.html'

    emps = Employee().query.order_by(sort_key)[offset:limit]


    return render_template(
        template,
        emps = emps
        )