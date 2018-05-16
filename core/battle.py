#!/usr/bin/python

import time
import json
import yaml
from string import Template
from discord import Embed
from core.common import make_embed
import core.creators as creators

with open('conf/battletext.yaml', 'r') as yamlf:
    TEXT = yaml.load(yamlf)

def dictsub(DICT, SUBS):

    TEMP = Template(json.dumps(DICT))
    return json.loads(TEMP.substitute(SUBS))

def gather_party(CNTDWN=None):
    
    SUBS = { 'cntdwn': CNTDWN }
    DATA = dictsub(TEXT['gather_party'], SUBS)
    if not CNTDWN:
        DATA.pop('fields', None)
    EMB = make_embed(DATA)
    return EMB

class battle(object):

    def __init__(self, PARTY):

        self.STATUS = True
        self.ENDSTATE = ''
        self.PARTY = PARTY
        self.MONSTER = creators.monster(PARTY.get_party_size())

    def go(self, TIMER):

        SUBS = { 'bar': self.MONSTER.get_hp_bar(),
                 'mondesc': self.MONSTER.DESC,
                 'timer': TIMER }
        DATA = dictsub(TEXT['action_lock_in'], SUBS)
        EMB = make_embed(DATA)
        return EMB
    
    def parties_turn(self, ACTIONS):

        RESULT = []
        SUBS = { 'bar': self.MONSTER.get_hp_bar(),
                 'mondesc': self.MONSTER.DESC,
                 'nick': '',
                 'action': '',
                 'actionresult': '' }
        DATA = dictsub(TEXT['parties_turn'], SUBS)
        DATA.pop('fields', None)
        EMB = make_embed(DATA)
        RESULT.append(EMB)
        for playerid, action in ACTIONS.items():
            SUBS['nick'] = self.PARTY.PLIST[playerid]['nick']
            SUBS['action'] = action
            SUBS['actionresult'] = self.do_action(action)
            DATA = dictsub(TEXT['parties_turn'], SUBS)
            EMB = make_embed(DATA)
            RESULT.append(EMB)
        return RESULT

    def monsters_turn(self):

        SUBS = { 'bar': self.MONSTER.get_hp_bar(),
                 'mondesc': self.MONSTER.DESC,
                 'dmg': self.MONSTER.DMG }
        DATA = dictsub(TEXT['enemies_turn'], SUBS)
        EMB = make_embed(DATA)
        return EMB

    def end_battle(self):

        SUBS = { 'endstate': self.ENDSTATE,
                 'mondesc': self.MONSTER.DESC }
        DATA = dictsub(TEXT[self.ENDSTATE.lower().rstrip('!')], SUBS)
        EMB = make_embed(DATA)
        return EMB

    def do_action(self, ACTION):

        if ACTION == '⚔':
            self.MONSTER.HP -= 1
            if self.MONSTER.HP <= 0:
                self.STATUS = False
                self.ENDSTATE = 'VICTORY!'
            return 'Attacks dealing 1 damage.'
        elif ACTION == '❇':
            self.PARTY.HP += 1
            return 'Heals the party for 1 HP'

async def start(CLIENT):

    BTLCHAN = CLIENT.get_channel('436221281457799178')
    await CLIENT.purge_from(BTLCHAN)
    while True:
        MSG = await CLIENT.send_message(BTLCHAN, embed=gather_party())
        RES = await CLIENT.wait_for_reaction(emoji='👍', message=MSG)
        #for cntdwn in range(10, 0, -1):
        #    await CLIENT.edit_message(MSG, embed=gather_party(CNTDWN=cntdwn))
        #    time.sleep(1)
        JOINED = await CLIENT.get_reaction_users(RES[0])
        PARTY = creators.party(JOINED)
        BTL = battle(PARTY)
        await CLIENT.clear_reactions(MSG)
        while BTL.STATUS == True:
            for cntdwn in range(10, 0, -1):
                MSG = await CLIENT.edit_message(MSG, embed=BTL.go(cntdwn))
                time.sleep(1)
            ACTIONS = {}
            for rctn in MSG.reactions:
                USERS = await CLIENT.get_reaction_users(rctn)
                for user in USERS:
                    ACTIONS[user.id] = rctn.emoji
            TURN = BTL.parties_turn(ACTIONS)
            await CLIENT.clear_reactions(MSG)
            for emb in TURN:
                await CLIENT.edit_message(MSG, embed=emb)
                await CLIENT.clear_reactions(MSG)
                time.sleep(2)
            await CLIENT.edit_message(MSG, embed=BTL.monsters_turn())
            await CLIENT.clear_reactions(MSG)
            time.sleep(2)
        await CLIENT.edit_message(MSG, embed=BTL.end_battle())
        await CLIENT.clear_reactions(MSG)
        time.sleep(5)
        await CLIENT.delete_message(MSG)
