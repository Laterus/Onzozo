#!/usr/local/bin/python3

import yaml
from tinydb import TinyDB, Query

DB = TinyDB('database/data.db', default_table='players')
Q = Query()
TABLE = DB.table('classes')

with open('conf/classdata.yaml', 'r') as yamlf:
    CONF = yaml.load(yamlf)

for section in CONF:
    CD = dict(CONF[section])
    CD.update({'name': section})
    TABLE.upsert(CD, Q.name == section)
