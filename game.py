#!/usr/local/bin/python3

import discord
import asyncio
import core.battle as battle

CLIENT = discord.Client()
for line in open('conf/token', 'r'):
    TOKEN = line.rstrip('\n')

async def setup():

    await battle.start(CLIENT)

@CLIENT.event
async def on_ready():
    print ('Logged in as '+CLIENT.user.name)
    await setup()

@CLIENT.event
async def on_reaction_add(reaction, user):
    try:
        if reaction.message.embeds[0]['author']['name'] == 'BATTLE!':
            if reaction.emoji != '👍':
                await CLIENT.remove_reaction(reaction.message,
                                             reaction.emoji, user)
        if reaction.message.embeds[0]['title'].startswith('Party'):
            for rctn in reaction.message.reactions:
                if rctn == reaction:
                    continue
                if user in await CLIENT.get_reaction_users(rctn):
                    await CLIENT.remove_reaction(reaction.message,
                                                 reaction.emoji, user)
            if reaction.emoji not in ['⚔', '🛡', '❇']:
                await CLIENT.remove_reaction(reaction.message,
                                             reaction.emoji, user)
    except IndexError:
        pass

@CLIENT.event
async def on_message(message):
    pass

CLIENT.run(TOKEN)
