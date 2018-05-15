#!/usr/local/bin/python3

import sys
sys.path.append('./')
import core.creators

print (core.creators.get_player_data(sys.argv[1]))
