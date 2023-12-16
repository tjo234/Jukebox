#!/usr/bin/env
import os
import sqlite3
from flask import g, current_app

class JukeboxDatabaseException(Exception):
    pass

def get_db_connection():
    # Check config value exists
    if not 'DATABASE' in current_app.config:
        raise JukeboxDatabaseException("The app.config['DATABASE'] is empty.")

    # Check that database exists
    DATABASE = current_app.config['DATABASE']
    if not os.path.exists(DATABASE):
            raise JukeboxDatabaseException("Path does does exist: %s" % DATABASE)
    
    # Load cached database connection
    db = getattr(g, '_database', None)

    # Open new database connection
    if not db:
        print(current_app.config)
        print('Opening SQL connection...')
        db = g._database = sqlite3.connect(DATABASE)     
    return db

class Database():
    @staticmethod
    def initialize():
        db = get_db_connection()
        with current_app.open_resource('database/schema.sql') as f:
            db.executescript(f.read().decode('utf8'))
    
    @staticmethod
    def close():
        print('Closing SQL connection...')
        get_db_connection().close()
        
    @staticmethod
    def executemany(sql, data):
        db = get_db_connection()
        cursor =  db.executemany(sql, data)  
        ret = cursor.rowcount
        db.commit()
        return ret

    @staticmethod
    def execute(sql):
        db = get_db_connection()
        cursor = db.execute(sql)
        ret = cursor.rowcount
        db.commit()
        return ret

    @staticmethod
    def fetch(sql):
        db = get_db_connection()
        ret = db.execute(sql).fetchall()
        return ret

    @staticmethod
    def get(sql):
        db = get_db_connection()
        ret = db.execute(sql).fetchone()
        return ret