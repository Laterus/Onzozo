#!/usr/local/bin/python3

import yaml
import json
from string import Template
from discord import Embed
from tinydb import TinyDB, Query

def make_embed(BASE, SUBS):

    TEMP = Template(json.dumps(BASE))
    DATA = json.loads(TEMP.substitute(SUBS), strict=False)
    EMB = Embed(title=DATA['title'],
                description=DATA['desc'],
                color=DATA['color'])
    EMB.set_author(name=DATA['author'])
    EMB.set_footer(text=DATA['footer'])
    if 'fields' in DATA:
        for f in DATA['fields']:
            EMB.add_field(name=f['name'], value=f['value'], inline=DATA['inline'])
    return EMB

def create_bar(CURPER):

    BAR = '['
    for hp in range(50):
        if hp <= CURPER:
            BAR = BAR + '|'
        else:
            BAR = BAR + '-'
    BAR = BAR + '] ' + str(CURPER*2) + '%'
    return BAR

def get_classes():

    with open('conf/classdata.yaml', 'r') as yamlf:
         return yaml.load(yamlf)

def check_player(ID):

    DB = TinyDB('database/data.db', default_table='players')
    Q = Query()
    TABLE = DB.table('players')
    return TABLE.search(Q.id == ID)
