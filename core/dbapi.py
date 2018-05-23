#!/usr/local/bin/python3

from tinydb import TinyDB, Query

class dbapi(object):

    def __init__(self):

        self.DB = TinyDB('database/data.db', default_table='players')
        self.Q = Query()

    def get_player_data(self, ID):

        TABLE = self.DB.table('players')
        DATA = TABLE.search(self.Q.id == str(ID))
        return DATA[0]

    def get_class_data(self, CLS):

        TABLE = self.DB.table('classes')
        DATA = TABLE.search(self.Q.name == CLS)
        return DATA[0]

    def get_skill_data(self, SKILL):

        TABLE = self.DB.table('skills')
        DATA = TABLE.search(self.Q.name == SKILL)
        return DATA[0]
