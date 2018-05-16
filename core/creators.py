#!/usr/local/bin/python3

import random
from tinydb import TinyDB, Query
from core.common import create_bar, get_classes

DB = TinyDB('database/data.db', default_table='players')
Q = Query()
CD = get_classes()

def get_player_data(ID):

    TABLE = DB.table('players')
    if not TABLE.search(Q.id == ID):
        SKEL = {'class_levels': {}}
        for cls in CD.keys():
            SKEL['class_levels'][cls] = 0
        SKEL.update({'id': ID})
        TABLE.insert(SKEL)
    PDATA = TABLE.search(Q.id == ID)
    return PDATA[0]

class party(object):

    def __init__(self, PLAYERS):

        self.HP = 10 + (2 * len(PLAYERS))
        self.PLIST = {}
        for player in PLAYERS:
            P = {}
            P['nick'] = player.display_name
            P['avatar'] = player.avatar_url
            P.update(get_player_data(player.id))
            self.PLIST[player.id] = P

    def get_party_size(self):

        return len(self.PLIST.keys())

def get_monster_data(MONSTERID):

    DB = TinyDB(MONSTERDB)
    Q = Query()
    MDATA = DB.search(Q.id == MONSTERID)
    return MDATA[0]

class monster(object):

    def __init__(self, MOD):
        '''
        self.TABLE = DB.table('monsters')
        LOW = MOD - 1
        HIGH = MOD + 1
        if LOW < 1:
            LOW = 1
        RANDID = random.randrange(LOW, HIGH+1)
        self.MDATA = self.TABLE(Q.id == RANDID)
        self.LEVEL = (1 * int(MOD))
        self.TYPE = 'Monster'
        self.DESC = 'Level '+str(self.LEVEL)+' '+self.TYPE
        self.HP = int(round((5 * self.LEVEL), 0))
        self.DMG = int(round(2 + int(MOD)))
        '''
        self.LEVEL = (1 * int(MOD))
        self.TYPE = 'Monster'
        self.DESC = 'Level '+str(self.LEVEL)+' '+self.TYPE
        self.MHP = int(round((5 * self.LEVEL), 0))
        self.HP = self.MHP
        self.DMG = int(round(2 + int(MOD)))

    def get_hp_bar(self):

        CURPER = int(round(self.HP / self.MHP, 2) * 50)
        return create_bar(CURPER)
