#!/usr/bin/env
from mpd import MPDClient
from flask import g

class JukeboxPlayerException(Exception):
    pass

def get_music_daemon():
    mpd = getattr(g, '_mpd', None)
    if not mpd:
        mpd = g._mpd = MPDClient()
        mpd.connect("jukebox.local", 6600)
    return mpd
  

def get_album_art(filename):
        print(filename)
        mpd = get_music_daemon()
        return mpd.readpicture(filename)

class JukeboxPlayer():

    @staticmethod
    def initialize():
        mpd = get_music_daemon()

        if len(mpd.playlist()) == 0:
            print("Updating playlist...")
            ret = mpd.findadd("artist", "Grateful Dead")

        mpd.play()   
        return mpd.status()     

    @staticmethod
    def status():
        mpd = get_music_daemon() 
        currentsong = mpd.currentsong()
        try:
            cover = mpd.albumart(currentsong['file'])
        except:
            cover = "/static/img/album.png"
        
        return {
            "version": mpd.mpd_version,
            "status": mpd.status(),
            "stats": mpd.stats(),
            "currentsong": currentsong,
            "playlist": mpd.playlist(),
            "cover": cover,
            "outputs": mpd.outputs()
        }

    @staticmethod
    def update():
        mpd = get_music_daemon() 
        ret = mpd.update()
        return {
            "status": ret,
            "stats": mpd.stats()
        }

    @staticmethod
    def cover(uri):
        return get_music_daemon().albumart(uri)

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

