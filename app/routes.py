# -*- coding: utf-8 -*-
from flask import render_template, request
from app import app, db
from app.models import Employee


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Sieger'}
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
