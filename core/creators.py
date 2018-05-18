#!/usr/local/bin/python3

from tinydb import TinyDB, Query

DB = TinyDB('database/data.db', default_table='players')
Q = Query()

def get_db_data(DBT, QUERY):

    TABLE = DB.table(DBT)
    if DBT == 'players':
        DATA = TABLE.search(Q.id == QUERY)
    else:
        DATA = TABLE.search(Q.name == QUERY)
    return DATA[0]

def create_starting_status(PLAYER, SLOT):

    P = {}
    P.update(get_db_data('players', PLAYER.id))
    CS = get_db_data('classes', P['current_class'])
    P['slot'] = str(SLOT)
    P['stats'] = CS['base_stats']
    P['stats']['maxhp'] = P['stats']['hp']
    SKILLS = {}
    for skl in CS['skills']:
        SKILLS[skl] = get_db_data('skills', skl)
    P['skills'] = SKILLS
    P['bnd'] = ''
    return P

def setup_player_party(PLAYERS):

    PLIST = {}
    NUM = 1
    for player in PLAYERS:
        PLIST[player.id] = create_starting_status(player, NUM)
        NUM += 1
    return PLIST

def generate_monster(MOD):

    LEVEL = (1 * int(MOD))
    TYPE = 'Monster'
    DESC = 'Level '+str(LEVEL)+' '+TYPE
    MHP = int(round((5 * LEVEL), 0))
    HP = MHP
    DMG = int(round(2 + int(MOD)))
    return { 1: {'name': 'Test Monster', 'slot': 1, 'stats': {'hp': 200, 'maxhp': 200} } }
