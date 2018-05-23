#!/usr/local/bin/python3

import yaml
import core.dbapi as dbapi
from core.common import dictsub, make_embed

def get_text():

    with open('conf/battle_lobby_text.yaml', 'r') as f:
        return yaml.load(f)

class battle_lobby(object):

    def __init__(self):

        self.COUNT = 1
        self.PARTIES = {}
        self.PLAYERS = {}

    def top_help_msg(self):

        TEXT = get_text()
        EMB = make_embed(TEXT['battle_lobby_top'])
        return EMB

    def cmdparse(self, MSG):

        try:
            PID = str(self.PLAYERS[MSG.author.id])
        except KeyError:
            PID = False
        if MSG.content == '//form':
            if not PID:
                self.create_party(MSG)
        elif MSG.content.startswith('//join'):
            if not PID:
                self.join_party(MSG)
        elif MSG.content == '//drop':
            if PID:
                DISBAND = self.PARTIES[PID].remove_member(MSG.author)
                if DISBAND:
                    for player in self.PARTIES[PID].get_member_ids():
                        self.PLAYERS.pop(player, None)
                    self.PARTIES.pop(PID, None)
                else:
                    self.PLAYERS.pop(MSG.author.id, None)

    def get_lobby_status(self):

        EMBS = {}
        for pid, party in self.PARTIES.items():
            EMBS[pid] = party.display_forming_status()
        return EMBS

    def create_party(self, MSG):

        PARTY = party(self.COUNT, MSG.author.id)
        self.PARTIES[str(self.COUNT)] = PARTY
        self.PLAYERS[MSG.author.id] = self.COUNT
        self.COUNT += 1

    def join_party(self, MSG):

        try:
            PID = MSG.content[2:].split(' ')[1]
            self.PARTIES[PID].add_member(MSG.author)
            self.PLAYERS[MSG.author.id] = PID
        except (IndexError, KeyError):
            return

class party(object):

    def __init__(self, ID, LEADER):

        self.ID = ID
        self.DB = dbapi.dbapi()
        LDR = self.DB.get_player_data(LEADER)
        self.PLIST = { 1: LDR['id'] }
        self.SUBS = { 'pid': str(self.ID),
                      's1': ':one:: :crown: %s' % LDR['name'],
                      's2': '[2]', 's3': '[3]', 's4': '[4]' }
        self.EMOJI = { 2: ':two:', 3: ':three:', 4: ':four:' }
        with open('conf/battletext.yaml', 'r') as f:
            self.TEXT = yaml.load(f)

    def display_forming_status(self):

        EMBD = dictsub(self.TEXT['form_party'], self.SUBS)
        return make_embed(EMBD)

    def add_member(self, PLAYER):

        PD = self.DB.get_player_data(PLAYER.id)
        NUM = [ i for i in range(2, 5) if i not in self.PLIST.keys() ][0]
        self.PLIST[NUM] = PD['id']
        self.SUBS['s'+str(NUM)] = self.EMOJI[NUM]+': %s' % PD['name']
        print (self.SUBS)

    def remove_member(self, PLAYER):

        for slot, player in self.PLIST.items():
            if player == str(PLAYER.id):
                if slot == 1:
                    return True
                self.PLIST.pop(slot, None)
                self.SUBS['s'+str(slot)] = '[%s]' % str(slot)

    def get_member_ids(self):

        return self.PLIST.values()

    def get_battle_ready(self):

        PARTY = {}
        for slot, playerid in self.PLIST.items():
            PLAYER = {}
            PLAYER.update(self.DB.get_player_data(playerid))
            CS = self.DB.get_class_data(PLAYER['current_class'])
            PLAYER['slot'] = str(SLOT)
            PLAYER['stats'] = CS['base_stats']
            PLAYER['stats']['maxhp'] = P['stats']['hp']
            SKILLS = {}
            for skl in CS['skills']:
                SKILLS[skl] = self.DB.get_skill_data(skl)
            PLAYER['skills'] = SKILLS
            PLAYER['bnd'] = ''
            PARTY[playerid] = PLAYER
        return PARTY

def generate_monster(MOD):

    LEVEL = (1 * int(MOD))
    TYPE = 'Monster'
    DESC = 'Level '+str(LEVEL)+' '+TYPE
    MHP = int(round((5 * LEVEL), 0))
    HP = MHP
    DMG = int(round(2 + int(MOD)))
    return { 1: {'name': 'Test Monster', 'slot': 1, 'stats': {'hp': 200, 'maxhp': 200} } }
