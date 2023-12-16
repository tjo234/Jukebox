#!/usr/bin/env
import os
import sqlite3
from flask import g, current_app

DB_KEY = "DATABASE"

class JukeboxDatabaseException(Exception):
    pass

def db_initialize():
    # Check config exists
    if not DB_KEY in current_app.config:
        raise JukeboxDatabaseException("The app.config['$s'] is empty." % DB_KEY)

    # If database exists, return True
    DATABASE = current_app.config[DB_KEY]
    if os.path.isfile(DATABASE):
        return True

    # Create DB schema and populate default values
    print('Initializing SQL database...')
    db = sqlite3.connect(DATABASE)  
    with current_app.open_resource('database/schema.sql') as f:
            db.executescript(f.read().decode('utf8'))
       

def get_db_connection():

    # Ensure DB is initialized
    db_initialize()

    # Load cached database connection
    db = getattr(g, '_database', None)

    # Open new database connection
    if not db:
        print('Opening SQL connection...')
        db = g._database = sqlite3.connect(current_app.config[DB_KEY])    

    return db

class Database():
    
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