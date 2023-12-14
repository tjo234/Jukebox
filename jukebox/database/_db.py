#!/usr/bin/env
import os
import sqlite3
from flask import g, current_app

FLASK_DATABASE = 'DATABASE'
class JukeboxLibraryNotFound(Exception):
    pass

def get_db_connection():
    if not FLASK_DATABASE in current_app.config:
        raise JukeboxLibraryNotFound("Environment varable does does exist: %s" % FLASK_DATABASE)

    DATABASE = current_app.config[FLASK_DATABASE]
    db = getattr(g, '_database', None)
    if db:
        print("Cached SQL connection:", DATABASE)
    else:
        if not os.path.exists(DATABASE):
            raise JukeboxLibraryNotFound("Path does does exist: %s" % DATABASE)
        db = g._database = sqlite3.connect(DATABASE)     
        print("Opened SQL connection:", DATABASE)
    return db

class Database():
    @staticmethod
    def initialize():
        db = get_db_connection()
        with current_app.open_resource('database/schema.sql') as f:
            db.executescript(f.read().decode('utf8'))

    @staticmethod
    def executemany(sql, data):
        db = get_db_connection()
        cursor =  db.executemany(sql, data)  
        ret = cursor.rowcount
        db.commit()
        db.close()
        return ret

    @staticmethod
    def execute(sql):
        db = get_db_connection()
        cursor = db.execute(sql)
        ret = cursor.rowcount
        db.commit()
        db.close()
        return ret

    @staticmethod
    def fetch(sql):
        db = get_db_connection()
        ret = db.execute(sql).fetchall()
        db.close()
        return ret

    @staticmethod
    def get(sql):
        db = get_db_connection()
        ret = db.execute(sql).fetchone()
        db.close()
        return ret