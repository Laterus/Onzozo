#!/usr/local/bin/python3

from discord import Embed

def make_embed(DATA):

    EMB = Embed(title=DATA['title'], description=DATA['desc'])
    EMB.set_author(name=DATA['author'])
    EMB.set_footer(text=DATA['footer'])
    for f in DATA['fields']:
        EMB.add_field(name=f['name'], value=f['value'], inline=DATA['inline'])
    return EMB
