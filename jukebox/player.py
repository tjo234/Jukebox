#!/usr/bin/env
from mpd import MPDClient, CommandError
from flask import g

from .library import get_album_art

class JukeboxPlayerException(Exception):
    pass

def get_mpd():
    mpd = getattr(g, '_mpd', None)
    if not mpd:
        mpd = g._mpd = MPDClient()
        mpd.connect("jukebox.local", 6600)
    return mpd
   
class JukeboxPlayer():

    @staticmethod
    def initialize():
        mpd = get_mpd()
        mpd.update()
        if int(mpd.status()['playlistlength']) == 0:
            mpd.findadd("any", "Grateful Dead")
        mpd.play()   
        return mpd.status()   

    @staticmethod
    def status():
        mpd = get_mpd()
        return {
            "version": mpd.mpd_version,
            "status": mpd.status(),
            "stats": mpd.stats(),
            "currentsong": mpd.currentsong(),
            "outputs": mpd.outputs()
        }
  
    @staticmethod
    def cover():
        mpd = get_mpd()
        try:
            cover = mpd.readpicture(mpd.currentsong()['file'])
            print(cover)
            return cover
        except Exception as ex:
            return None

    @staticmethod
    def playlist():
        return get_mpd().playlistinfo()

    @staticmethod
    def listplaylist(pid):
        return get_mpd().listplaylist(pid)

    @staticmethod
    def update():
        mpd = get_mpd() 
        ret = mpd.update()
        return mpd.status()

    @staticmethod
    def artists():
        return get_mpd().list('artist')

    @staticmethod
    def albums():
        return get_mpd().list('album')

    @staticmethod
    def random():
        mdb = get_mpd()
        random = int(mdb.status()['random'])
        print('random: %s' % random)
        if random == 0: 
            return mdb.random(1)
        else:
            return mdb.random(0)

    @staticmethod
    def repeat():
        mdb = get_mpd()
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
        mdb = get_mpd()
        is_muted = (int(mdb.status()['volume']) == 0)
        if is_muted:
            return mdb.setvol(100)
        else:
            return mdb.setvol(0)

    @staticmethod
    def volume(vol):
        return get_mpd().setvol(vol)

    @staticmethod
    def library():
        return get_mpd().listall()

    @staticmethod
    def play():
        return get_mpd().play()

    @staticmethod
    def pause():
        return get_mpd().pause()

    @staticmethod
    def stop():
        return get_mpd().stop()

    @staticmethod
    def next():
        return get_mpd().next()

    @staticmethod
    def previous():
        return get_mpd().previous()

    @staticmethod
    def listneighbors():
        return get_mpd().listneighbors()

    @staticmethod
    def listmounts():
        return get_mpd().listmounts()

    @staticmethod
    def ping():
        return get_mpd().ping()

    @staticmethod
    def idle():
        return get_mpd().idle()

    @staticmethod
    def outputs():
        return get_mpd().outputs()

    @staticmethod
    def status_only():
        return get_mpd().status()

    @staticmethod
    def playlist_reset():
        return get_mpd().clear()

        

