#!/usr/bin/env
from ._db import Database

class Track():
    @staticmethod
    def get_track(filename):
        sql = '''
            SELECT * FROM tracks 
            WHERE filename = "%s";
        ''' % filename
        t = Database.get(sql)
        return to_dict(t)

    @staticmethod
    def get_tracks():
        sql = "SELECT * FROM tracks ORDER BY filename;"
        return [to_dict(t) for t in Database.fetch(sql)]

    @staticmethod
    def get_artists():
        sql = '''
            SELECT albumartist, count(*) FROM tracks 
            GROUP BY albumartist;
        '''
        return Database.fetch(sql)

    @staticmethod
    def get_albums():
        sql = '''
            SELECT album, count(*) FROM tracks 
            GROUP BY album;
        '''
        return Database.fetch(sql)

    @staticmethod
    def get_genres():
        sql = '''
            SELECT genre, count(*) FROM tracks 
            GROUP BY genre;
        '''
        return Database.fetch(sql)

    @staticmethod
    def create(data):
        print(data)
        sql = '''
            INSERT INTO tracks(filename, track, artist, albumartist, album, genre, year, tracknumber, discnumber) 
            VALUES(:filename, :track, :artist, :albumartist, :album, :genre, :year, :tracknumber, :discnumber)
            ON CONFLICT DO NOTHING;
        '''
        return Database.executemany(sql, data) 

    @staticmethod
    def delete(filename):
        print("Track.delete")
        sql = '''
            DELETE FROM tracks 
            WHERE filename = "%s";
        ''' % filename
        return Database.execute(sql) 

def to_dict(track):
    if not track:
        return None
    return {
        "filename": track[0],
        "track": track[1],
        "artist": track[2],
        "albumartist": track[3],
        "album": track[4],
        "genre": track[5],
        "year": track[6],
        "tracknumber": track[7],
        "discnumber": track[8],
        "added_on": track[9],
        "updated_on": track[10]
    }
