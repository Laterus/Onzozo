#!/usr/local/bin/python3

import sys
sys.path.append('./')
import core.creators

TYPES = ['Goblin', 'Golem', 'Orc',
         'Wombat', 'Chipmunk', 'Brute',
         'Swashbuckler', 'Monkey', 'Bob']

print (core.creators.get_player_data(sys.argv[1]))
