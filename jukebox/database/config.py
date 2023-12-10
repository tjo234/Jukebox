#!/usr/bin/env
from ._db import Database

class Config():
    @staticmethod
    def fetch():
        sql = "SELECT * FROM config ORDER BY id"
        return Database.fetch(sql)

    @staticmethod
    def get(config_id):
        sql = """
            SELECT * FROM config WHERE id = "%s" 
        """ % config_id
        return Database.get(sql)[1]

    @staticmethod
    def set(config_id, value):
        sql = """
            INSERT OR REPLACE INTO config(config_id, value)
            VALUES(?, ?);
        """
        return Database.execute(sql, data)