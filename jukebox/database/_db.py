#!/usr/bin/env
import sqlite3
from flask import current_app

def get_db_connection():
    return sqlite3.connect("data/library.db")

class Database():
    @staticmethod
    def initialize():
        db = get_db_connection()
        with current_app.open_resource('jukebox/database/schema.sql') as f:
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