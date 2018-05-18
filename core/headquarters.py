#!/usr/local/bin/python3

import time
import yaml
from tinydb import TinyDB, Query
from core.common import make_embed, check_player

DB = TinyDB('database/data.db', default_table='players')
Q = Query()

with open('conf/headquarterstext.yaml', 'r') as yamlf:
    TEXT = yaml.load(yamlf)

with open('conf/classdata.yaml', 'r') as yamlf:
    CD = yaml.load(yamlf)

def check_player(ID):

    TABLE = DB.table('players')
    return TABLE.search(Q.id == ID)

def create_profile(PLAYER, CLS):

    TABLE = DB.table('players')
    SKEL = { 'id': PLAYER.id,
             'name': PLAYER.display_name,
             'avatar': PLAYER.avatar_url,
             'current_class': CLS,
             'current_class_level': 1,
             'class_levels': {} }
    for cls in CD.keys():
        SKEL['class_levels'][cls] = 1
    TABLE.insert(SKEL)

def delete_profile(ID):

    TABLE = DB.table('players')
    DOC = TABLE.get(Q.id == ID)
    TABLE.remove(doc_ids=[DOC.doc_id])

async def create(CLIENT, MSG):

    CLSCHO = ''
    for k, v in CD.items():
        CLSCHO = CLSCHO + k + ' -\n    ' + v['desc'] + '\n\n'
    SUBS = { 'nick': MSG.author.display_name,
             'classchoices': CLSCHO }
    EMB = make_embed(TEXT['createstart'], SUBS)
    CRMSG = await CLIENT.send_message(MSG.channel, embed=EMB)
    def check_choice(message):
        return message.content.lower().capitalize() in CD.keys()
    CCMSG = await CLIENT.wait_for_message(timeout=20, author=MSG.author, check=check_choice)
    if not CCMSG:
        EMB = make_embed(TEXT['createtimeout'], SUBS)
        await CLIENT.edit_message(CRMSG, embed=EMB)
    else:
        create_profile(MSG.author, CCMSG.content)
        EMB = make_embed(TEXT['createend'], SUBS)
        await CLIENT.edit_message(CRMSG, embed=EMB)
    async for msg in CLIENT.logs_from(MSG.channel):
        if msg.author == MSG.author:
            await CLIENT.delete_message(msg)
    time.sleep(5)
    await CLIENT.delete_message(CRMSG)

async def delete(CLIENT, MSG):

    SUBS = { 'nick': MSG.author.display_name }
    EMB = make_embed(TEXT['deleteconfirm'], SUBS)
    DCMSG = await CLIENT.send_message(MSG.channel, embed=EMB)
    DRMSG = await CLIENT.wait_for_message(timeout=20,
                                          author=MSG.author,
                                          content='YESDELETEITOMG')
    if DRMSG:
        delete_profile(MSG.author.id)
        EMB = make_embed(TEXT['deleteend'], SUBS)
        await CLIENT.edit_message(DCMSG, embed=EMB)
    async for msg in CLIENT.logs_from(MSG.channel):
        if msg.author == MSG.author:
            await CLIENT.delete_message(msg)
    await CLIENT.delete_message(DCMSG)

async def parse(CLIENT, MSG):

    if MSG.content.startswith('!create'):
        if check_player(MSG.author.id):
            EMB = make_embed(TEXT['createexists'], {'nick': MSG.author.display_name})
            EMSG = await CLIENT.send_message(MSG.channel, embed=EMB)
            time.sleep(5)
            await CLIENT.delete_messages([EMSG, MSG])
        else:
            await create(CLIENT, MSG)
    elif MSG.content.startswith('!update'):
        pass
    elif MSG.content.startswith('!delete'):
        if not check_player(MSG.author.id):
            EMB = make_embed(TEXT['deleteexists'], {'nick': MSG.author.display_name})
            EMSG = await CLIENT.send_message(MSG.channel, embed=EMB)
            time.sleep(5)
            await CLIENT.delete_messages([EMSG, MSG])
        else:
            await delete(CLIENT, MSG)

async def start(CLIENT):

    HQRCHAN = CLIENT.get_channel('446314223967141888')
    await CLIENT.purge_from(HQRCHAN)
    MSG = await CLIENT.send_message(HQRCHAN, embed=make_embed(TEXT['top'], {}))
