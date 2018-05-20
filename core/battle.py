#!/usr/local/bin/python3

import time
import json
import yaml
from discord import Embed
from core.common import make_embed, dictsub
import core.creators as creators

with open('conf/battletext.yaml', 'r') as yamlf:
    TEXT = yaml.load(yamlf)
with open('conf/formulas.yaml', 'r') as yamlf:
    FORMULAS = yaml.load(yamlf)['battle']

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
        TEMP = TEXT['enemy_party'].copy()
        FIELDS = TEMP.pop('fields')
        TEMP['fields'] = []
        for monster in self.MONSTERS.keys():
            MON = self.MONSTERS[monster].copy()
            MON['hpbar'] = get_hpbar(MON)
            TEMP['fields'].append(dictsub(FIELDS[0], MON))
        EMBD = dictsub(TEMP, SUBS)
        return make_embed(EMBD)

    def player_party(self):

        SUBS = {}
        TEMP = TEXT['player_party'].copy()
        FIELDS = TEMP.pop('fields')
        TEMP['fields'] = []
        for player in self.PARTY.keys():
            MEM = self.PARTY[player].copy()
            MEM['hpbar'] = get_hpbar(MEM)
            TEMP['fields'].append(dictsub(FIELDS[0], MEM))
        EMBD = dictsub(TEMP, SUBS)
        return make_embed(EMBD)

    def cmdparse(self, MSG):

        ACTION = MSG.content[2:].lower().split(' ')
        PLAYER = self.PARTY[MSG.author.id]
        if ACTION[0] in PLAYER['skills'].keys():
            SKLD = PLAYER['skills'][ACTION[0]]
            if len(ACTION) < 2:
                TARGET = 1
            else:
                TARGET = ACTION[1]
            self.do_action(SKLD, PLAYER, TARGET)

    def do_action(self, SKLD, PLAYER, TARGET):

        SUBS = SKLD.copy()
        SUBS['mod'] = PLAYER['stats'][SKLD['mod']]
        if SKLD['target'] == 'enemy':
            if TARGET not in self.MONSTERS:
                TARGET = 1
            for t in  SKLD['type']:
                FTEMP = FORMULAS[t]
                FORMRES = eval(dictsub(FTEMP, SUBS))
                if t == 'damage':
                    self.MONSTERS[TARGET]['stats']['hp'] -= FORMRES

async def msgparse(MSG):

    try:
        BTL.cmdparse(MSG)
    except NameError:
        pass

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

    global BTL
    BTLCHAN = CLIENT.get_channel('436221281457799178')
    await CLIENT.purge_from(BTLCHAN)

    while True:
        JOINED = await gather_party(CLIENT, BTLCHAN)
        PARTY = creators.setup_player_party(JOINED)
        MONSTERS = creators.generate_monster(1)
        BTL = battle(PARTY, MONSTERS)
        MPMSG = await CLIENT.send_message(BTLCHAN, embed=BTL.monster_party())
        PPMSG = await CLIENT.send_message(BTLCHAN, embed=BTL.player_party())
        COUNT = 0
        while BTL.STATUS == True:
            await CLIENT.edit_message(MPMSG, embed=BTL.monster_party())
            await CLIENT.edit_message(PPMSG, embed=BTL.player_party())
            time.sleep(.1)
            COUNT += 1
