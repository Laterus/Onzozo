#!/usr/local/bin/python3

import yaml
from core.common import make_embed

with open('conf/introtext.yaml', 'r') as yamlf:
    TEXT = yaml.load(yamlf)

async def start(CLIENT):

    INTCHAN = CLIENT.get_channel('446315742942593024')
    await CLIENT.purge_from(INTCHAN)
    MSG = await CLIENT.send_message(INTCHAN, embed=make_embed(TEXT['introduction'], {}))
