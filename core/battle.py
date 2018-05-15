#!/usr/bin/python

import time
import json
import yaml
from string import Template
from discord import Embed
from core.common import make_embed
from core.monster import monster
import core.creators as creators

with open('conf/battletext.yaml', 'r') as yamlf:
    TEXT = yaml.load(yamlf)

def dictsub(DICT, SUBS):

    TEMP = Template(json.dumps(DICT))
    return json.loads(TEMP.substitute(SUBS))

def gather_party(CNTDWN=None):
    
    if CNTDWN:
        TEMP = Template(json.dumps(TEXT['gather_party']))
        DATA = json.loads(TEMP.substitute({'cntdwn': CNTDWN}))
        EMB = make_embed(DATA)
    else:
        EMB = Embed(title=TEXT['gather_party']['title'],
                    description=TEXT['gather_party']['desc'])
        EMB.set_author(name=TEXT['gather_party']['author'])
    return EMB

def create_bar(AMT):

    BAR = '('
    for hp in range(AMT):
        BAR = BAR + '='
    BAR = BAR + ')'
    return BAR

class battle(object):

    def __init__(self, PARTY):

        self.STATUS = True
        self.ENDSTATE = ''
        self.PARTY = PARTY
        self.MONSTER = monster(PARTY.get_party_size())

    def go(self, TIMER):

        EMB = Embed(title='Party HP: '+str(self.PARTY.HP),
                    description='React to this message with the action you will take!')
        EMB.set_author(name=self.MONSTER.DESC + ' // HP: ' + str(self.MONSTER.HP))
        EMB.add_field(name=':crossed_swords: Attack',
                      value='Deals 1 damage', inline=True)
        EMB.add_field(name=':sparkle: Heal',
                      value='Party regains 1 HP', inline=True)
        EMB.set_footer(text='Timer: [%s]' % TIMER)
        return EMB
    
    def parties_turn(self, ACTIONS):

        RESULT = []
        EMB = Embed(title='Party HP: '+create_hp_bar(self.PARTY.HP),
                    description='Party takes its turn...')
        EMB.set_author(name=self.MONSTER.DESC + ' // HP: ' + create_hp_bar(self.MONSTER.HP))
        EMB.set_footer(text='Monster is readying an attack...')
        RESULT.append(EMB)
        for playerid, action in ACTIONS.items():
            EMB = Embed(title='Party HP: '+create_hp_bar(self.PARTY.HP),
                        description='Party takes its turn...')
            EMB.set_author(name=self.MONSTER.DESC + ' // HP: ' + create_hp_bar(self.MONSTER.HP))
            EMB.set_footer(text='Monster is readying an attack...')
            NICK = self.PARTY.PLIST[playerid]['nick']
            ACT = self.do_action(action)
            EMB.add_field(name=NICK + ' - ' + action, value=ACT, inline=False)
            RESULT.append(EMB)
        return RESULT

    def monsters_turn(self):

        EMB = Embed(title='Party HP: '+create_hp_bar(self.PARTY.HP),
                    description='Monster takes its turn...')
        EMB.set_author(name=self.MONSTER.DESC + ' // HP: ' + create_hp_bar(self.MONSTER.HP))
        EMB.add_field(name='Monster', value='Attacks for %s damage!' % str(self.MONSTER.DMG))
        self.PARTY.HP -= self.MONSTER.DMG
        if self.PARTY.HP <= 0:
            self.STATUS = False
            self.ENDSTATE = 'DEFEAT!'
        return EMB

    def end_battle(self):

        if self.ENDSTATE == 'VICTORY!':
            EMB = Embed(title='Your party has successfully beat the %s' % self.MONSTER.DESC,
                        description='Check out the loot!')
        elif self.ENDSTATE == 'DEFEAT!':
            EMB = Embed(title='Your party has succumb to the %s' % self.MONSTER.DESC,
                        description='No loot awarded!')
        EMB.set_author(name=self.ENDSTATE)
        EMB.set_footer(text='(loot not yet implemented)')
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
        for cntdwn in range(10, 0, -1):
            await CLIENT.edit_message(MSG, embed=gather_party(CNTDWN=cntdwn))
            time.sleep(1)
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
                time.sleep(2)
            await CLIENT.edit_message(MSG, embed=BTL.monsters_turn())
            time.sleep(2)
        await CLIENT.edit_message(MSG, embed=BTL.end_battle())
        time.sleep(5)
        await CLIENT.delete_message(MSG)
