from seeder import ResolvingSeeder
from app import app, db
from app.models import Employee
import psycopg2, time

import json
from datetime import *
import random

seeder = ResolvingSeeder(db.session)

try:
    seeder.register_class(Employee)
except AttributeError:
    print('AttrErr')

with open('./data_init.json','r') as file:
    emp = json.loads(file.read())

manager_positions = ['director', 'manager', 'department chief', 'team leader']
workers = ['driver', 'administrator', 'dispatcher', 'sales', 'controller']


managers = set()
for _ in emp:
    managers.add(_['manager_id'])
for e in emp:
    e['work_start'] = datetime.strptime(e['work_start'], "%d/%m/%Y")
    if e['id'] in managers:
        e['position'] = random.choice(manager_positions)
    else:
        e['position'] = random.choice(workers)


emp[0]['manager_id'] = None
emp[0]['position'] = " The President"

emp = [{"target_class": "Employee", "data": emp}]

seeder.load_entities_from_data_dict(emp)

db.session.commit()
