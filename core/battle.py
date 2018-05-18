#!/usr/local/bin/python3

import time
import json
import yaml
from discord import Embed
from core.common import make_embed, dictsub
import core.creators as creators

with open('conf/battletext.yaml', 'r') as yamlf:
    TEXT = yaml.load(yamlf)

def get_hpbar(MEM):

    BARSIZE = 20
    PERDEC = round(MEM['stats']['hp'] / MEM['stats']['maxhp'], 2)
    CURPER = int(PERDEC * 100)
    NOTCHES = int(PERDEC * BARSIZE)
    BAR = '['
    for hp in range(BARSIZE):
        if hp <= NOTCHES:
            BAR = BAR + '|'
        else:
            BAR = BAR + '-'
    BAR = BAR + '] ' + str(CURPER) + '%'
    return BAR

def gen_cooldown(SECS):

    for sec in range(SECS, 1, -1):
        yield sec

class battle(object):

    def __init__(self, PARTY, MONSTERS):

        self.STATUS = True
        self.ENDSTATE = ''
        self.PARTY = PARTY
        self.MONSTERS = MONSTERS

    def monster_party(self):

        SUBS = {}
        TEMP = TEXT['enemy_party']
        FIELDS = TEMP.pop('fields')
        TEMP['fields'] = []
        for monster in self.MONSTERS.keys():
            MON = self.MONSTERS[monster]
            MON['hpbar'] = get_hpbar(MON)
            TEMP['fields'].append(dictsub(FIELDS[0], MON))
        EMBD = dictsub(TEMP, SUBS)
        return make_embed(EMBD)

    def player_party(self):

        SUBS = {}
        TEMP = TEXT['player_party']
        FIELDS = TEMP.pop('fields')
        TEMP['fields'] = []
        for player in self.PARTY.keys():
            MEM = self.PARTY[player]
            MEM['hpbar'] = get_hpbar(MEM)
            TEMP['fields'].append(dictsub(FIELDS[0], MEM))
        EMBD = dictsub(TEMP, SUBS)
        return make_embed(EMBD)

    def parse(self, MSG):

        ACTION = MSG.content[2:].lower().split(' ')
        PLAYER = self.PARTY[MSG.author.id]
        LOWSKL = [ skill.lower() for skill in PLAYER['skills'].keys() ]
        if ACTION[0] in LOWSKL:
            if len(ACTION) < 2:
                TARGET = 1
            else:
                TARGET = ACTION[1]
            self.do_action(ACTION[0], PLAYER, TARGET)

    def do_action(self, ACTION, PLAYER, TARGET):
        print (ACTION, PLAYER, TARGET)

async def gather_party(CLIENT, BTLCHAN):

    BASE = TEXT['gather_party']
    BASECNT = TEXT['gather_party_cntdwn']
    MSG = await CLIENT.send_message(BTLCHAN, embed=make_embed(BASE))
    RES = await CLIENT.wait_for_reaction(emoji='👍', message=MSG)
    #for cntdwn in range(10, 0, -1):
    #    SUBS = { 'cntdwn': cntdwn }
    #    EMBD = dictsub(BASECNT, SUBS)
    #    await CLIENT.edit_message(MSG, embed=make_embed(EMBD))
    #    time.sleep(1)
    PARTY = await CLIENT.get_reaction_users(RES[0])
    await CLIENT.delete_message(MSG)
    return PARTY

async def start(CLIENT):

    BTLCHAN = CLIENT.get_channel('436221281457799178')
    await CLIENT.purge_from(BTLCHAN)

    @CLIENT.event
    async def on_message(message):
        if message.channel != BTLCHAN:
            pass
        if message.content.startswith('//'):
            try:
                BTL.parse(message)
            except NameError:
                pass
            await CLIENT.delete_message(message)
        else:
            if not message.author.bot:
                await CLIENT.delete_message(message)

    while True:
        JOINED = await gather_party(CLIENT, BTLCHAN)
        PARTY = creators.setup_player_party(JOINED)
        MONSTERS = creators.generate_monster(1)
        BTL = battle(PARTY, MONSTERS)
        COUNT = 0
        MPMSG = await CLIENT.send_message(BTLCHAN, embed=BTL.monster_party())
        PPMSG = await CLIENT.send_message(BTLCHAN, embed=BTL.player_party())
        while BTL.STATUS == True:
            await CLIENT.edit_message(MPMSG, embed=BTL.monster_party())
            await CLIENT.edit_message(PPMSG, embed=BTL.player_party())
            time.sleep(1)
            COUNT += 1
