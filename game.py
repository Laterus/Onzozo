#!/usr/local/bin/python3

import discord
import asyncio
import core.battle_lobby as battle_lobby
from core.common import SERVSET

CLIENT = discord.Client()

@CLIENT.event
async def on_ready():
    print ('Logged in as '+CLIENT.user.name)
    await setup_battle_lobby()

@CLIENT.event
async def on_reaction_add(reaction, user):
    pass

async def setup_battle_lobby():

    @CLIENT.event
    async def on_message(message):
        if not message.channel.name == 'battle_lobby':
            return
        if message.content.startswith('//'):
            BTLLOB.cmdparse(message)
            await message.delete()
        else:
            if message.author != CLIENT.user:
                await message.delete()

    G = CLIENT.get_guild(SERVSET['server']['id'])
    for category in G.categories:
        if category.name == 'Onzozo':
            C = category
    for chan in C.channels:
        if chan.name == 'battle_lobby':
            BTLLOBCHAN = chan
    BTLLOB = battle_lobby.battle_lobby()
    await BTLLOBCHAN.purge()
    TOPMSG = await BTLLOBCHAN.send(embed=BTLLOB.top_help_msg())
    while True:
        STATUS = BTLLOB.get_lobby_status()
        async for msg in BTLLOBCHAN.history():
            try:
                PID = msg.embeds[0].author.name.split(' ')[0]
            except (ValueError, IndexError):
                pass
            if PID not in STATUS.keys():
                if not msg.id == TOPMSG.id:
                    await msg.delete()
            elif PID in STATUS.keys():
                print (PID)
                await msg.edit(embed=STATUS.pop(PID))
            for pid, emb in STATUS.items():
                await BTLLOBCHAN.send(embed=STATUS[pid])
        await asyncio.sleep(2)

def main():

    for line in open(SERVSET['tokenfile'], 'r'):
        TOKEN = line.rstrip('\n')
    CLIENT.run(TOKEN)

if __name__ == '__main__':
    main()
