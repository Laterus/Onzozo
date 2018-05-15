#!/usr/local/bin/python3

import random
from tinydb import TinyDB, Query

DB = TinyDB('database/data.db', default_table='players')
Q = Query()

def get_player_data(NAME):

    TABLE = DB.table('players')
    if not TABLE.search(Q.name == NAME):
        TABLE.upsert({'name': NAME})
    PDATA = TABLE.search(Q.name == NAME)
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
