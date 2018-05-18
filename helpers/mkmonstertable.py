#!/usr/local/bin/python3

import yaml
from tinydb import TinyDB, Query

DB = TinyDB('database/data.db', default_table='players')
Q = Query()
DB.purge_table('monsters')
TABLE = DB.table('monsters')

with open('conf/monster.yaml', 'r') as yamlf:
    CONF = yaml.load(yamlf)

for section in CONF:
    CD = dict(CONF[section])
    CD.update({'name': section})
    TABLE.upsert(CD, Q.name == section)
