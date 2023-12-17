#!/usr/bin/env
from mpd import MPDClient, CommandError
from flask import g

from .library import get_album_art

class JukeboxPlayerException(Exception):
    pass

def get_music_daemon():
    mpd = getattr(g, '_mpd', None)
    if not mpd:
        mpd = g._mpd = MPDClient()
        mpd.connect("jukebox.local", 6600)
    return mpd
   
class JukeboxPlayer():

    @staticmethod
    def initialize():
        mpd = get_music_daemon()
        mpd.play()   
        return mpd.status()   

    @staticmethod
    def status():
        mpd = get_music_daemon()
        song = mpd.currentsong()
        uri = None
        albumart = None
        embedded = None
        cover = None

        try:
            uri = "/var/lib/mpd/music/" + song['file']
        except Exception as ex:
            print(ex)
            None

        if uri:
            try:
                albumart = mpd.albumart(uri)
            except Exception as ex:
                print(ex)
                None
            
            try:
                embedded = mpd.readpicture(uri)
            except Exception as ex:
                print(ex)
                None

            try:
                cover = get_album_art(uri)
            except Exception as ex:
                print(ex)
                None
        
        return {
            "version": mpd.mpd_version,
            "status": mpd.status(),
            "stats": mpd.stats(),
            "currentsong": song,
            "outputs": mpd.outputs(),
            "cover": {
                "albumart": albumart,
                "embedded": embedded,
                "mutagen": cover,
                "default": "/static/img/album.png"
            }
        }

    @staticmethod
    def playlist():
        return get_music_daemon().playlistinfo()

    @staticmethod
    def listplaylist(pid):
        return get_music_daemon().listplaylist(pid)

    @staticmethod
    def update():
        mpd = get_music_daemon() 
        ret = mpd.update()
        return mpd.status()

    @staticmethod
    def artists():
        return get_music_daemon().list('artist')

    @staticmethod
    def albums():
        return get_music_daemon().list('album')

    @staticmethod
    def library():
        return get_music_daemon().listall()

    @staticmethod
    def play():
        return get_music_daemon().play()

    @staticmethod
    def pause():
        return get_music_daemon().pause()

    @staticmethod
    def stop():
        return get_music_daemon().stop()

    @staticmethod
    def next():
        return get_music_daemon().next()

    @staticmethod
    def previous():
        return get_music_daemon().previous()

    @staticmethod
    def random():
        mdb = get_music_daemon()
        random = int(mdb.status()['random'])
        print('random: %s' % random)
        if random == 0: 
            return mdb.random(1)
        else:
            return mdb.random(0)

    @staticmethod
    def repeat():
        mdb = get_music_daemon()
        repeat = int(mdb.status()['repeat'])
        single = int(mdb.status()['single'])

        # 1 - OFF / OFF - Repeat OFF
        # 2 - ON / OFF  - Repeat ALL
        # 3 - ON / ON   - Repeat ONE

        if repeat == 0 and single == 0:
            mdb.repeat(1)
        elif repeat == 1 and single == 0:
            mdb.single(1)
        else:
            mdb.single(0)
            mdb.repeat(0)
        return True

    @staticmethod
    def mute():
        mdb = get_music_daemon()
        is_muted = (int(mdb.status()['volume']) == 0)
        if is_muted:
            return mdb.setvol(100)
        else:
            return mdb.setvol(0)

    @staticmethod
    def volume(vol):
        return get_music_daemon().setvol(vol)

    @staticmethod
    def listneighbors():
        return get_music_daemon().listneighbors()

    @staticmethod
    def listmounts():
        return get_music_daemon().listmounts()

    @staticmethod
    def ping():
        return get_music_daemon().ping()

    @staticmethod
    def idle():
        return get_music_daemon().idle()

    @staticmethod
    def outputs():
        return get_music_daemon().outputs()

    @staticmethod
    def status_only():
        return get_music_daemon().status()

    @staticmethod
    def playlist_reset():
        db = get_music_daemon()
        db.clear()
        db.findadd("any", "A Tribe Called Quest")
        db.play()

        

