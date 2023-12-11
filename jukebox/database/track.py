#!/usr/bin/env
from ._db import Database

class Track():
    @staticmethod
    def get_track_by_path(filename):
        sql = '''
            SELECT ROWID, * FROM tracks 
            WHERE filename = "%s";
        ''' % filename
        return to_dict(Database.get(sql))

    @staticmethod
    def get_track_by_id(track_id):
        sql = '''
            SELECT ROWID, * FROM tracks 
            WHERE ROWID = %s;
        ''' % track_id
        return to_dict(Database.get(sql))

    @staticmethod
    def get_tracks():
        sql = "SELECT ROWID, * FROM tracks ORDER BY artist, album, track;"
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
        "id": track[0],
        "filename": track[1],
        "track": track[2],
        "artist": track[3],
        "albumartist": track[4],
        "album": track[5],
        "genre": track[6],
        "year": track[7],
        "tracknumber": track[8],
        "discnumber": track[9],
        "added_on": track[10],
        "updated_on": track[11]
    }
