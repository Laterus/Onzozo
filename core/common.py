#!/usr/local/bin/python3

import yaml
import json
from trender import TRender
from discord import Embed
from tinydb import TinyDB, Query

DB = TinyDB('database/data.db', default_table='players')
Q = Query()

def get_db_data(DBT, QUERY):

    TABLE = DB.table(DBT)
    if DBT == 'players':
        DATA = TABLE.search(Q.id == QUERY)
    else:
        DATA = TABLE.search(Q.name == QUERY)
    return DATA[0]

with open('conf/server_settings.yaml') as f:
    SERVSET = yaml.load(f)

def dictsub(DICT, SUBS):

    TEMP = TRender(json.dumps(DICT))
    return json.loads(TEMP.render(SUBS), strict=False)

def make_embed(DATA):

    EMB = Embed(title=DATA['title'],
                description=DATA['desc'],
                color=DATA['color'])
    EMB.set_author(name=DATA['author']['name'])
    EMB.set_footer(text=DATA['footer'])
    if 'fields' in DATA:
        for f in DATA['fields']:
            EMB.add_field(name=f['name'], value=f['value'], inline=DATA['inline'])
    return EMB

def check_player(ID):

    DB = TinyDB('database/data.db', default_table='players')
    Q = Query()
    TABLE = DB.table('players')
    return TABLE.search(Q.id == ID)
