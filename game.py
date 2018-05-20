#!/usr/local/bin/python3

import discord
import asyncio
import core.intro as intro
import core.headquarters as headquarters
import core.battle as battle
from core.common import SERVSET

CLIENT = discord.Client()
for line in open(SERVSET['tokenfile'], 'r'):
    TOKEN = line.rstrip('\n')

async def setup():

    #await intro.start(CLIENT)
    #await headquarters.start(CLIENT)
    await battle.start(CLIENT)

@CLIENT.event
async def on_ready():
    print ('Logged in as '+CLIENT.user.name)
    await setup()

@CLIENT.event
async def on_reaction_add(reaction, user):
    pass

@CLIENT.event
async def on_message(message):
    if message.channel.id not in SERVSET['channels'].values():
        return
    if message.content.startswith('//'):
        await battle.msgparse(message)
        await CLIENT.delete_message(message)
    elif message.channel.name == 'headquarters' and message.content.startswith('!'):
        await headquarters.parse(CLIENT, message)
    else:
        if message.author != CLIENT.user:
            await CLIENT.delete_message(message)

CLIENT.run(TOKEN)
