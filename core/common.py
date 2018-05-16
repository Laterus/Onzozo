#!/usr/local/bin/python3

from discord import Embed

def make_embed(DATA):

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
