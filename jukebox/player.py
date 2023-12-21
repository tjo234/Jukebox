#!/usr/bin/env
from mpd import MPDClient, CommandError
from flask import g

from .utils import duration_to_time

class JukeboxPlayerException(Exception):
    pass

def get_mpd():
    mpd = getattr(g, '_mpd', None)
    if not mpd:
        mpd = g._mpd = MPDClient()
        mpd.connect("jukebox.local", 6600)
    return mpd

def get_status():
    mpd = get_mpd()

    # Check for cover.jpg in album folder 
    has_folder_cover = False
    try:
        has_folder_cover = ('binary' in mpd.albumart(mpd.currentsong()['file']))
    except Exception as ex:
        pass

    # Check for embedded id3 cover
    has_embedded_cover = False
    try:
        has_embedded_cover = ('binary' in mpd.readpicture(mpd.currentsong()['file']))
    except Exception as ex:
        pass

    cover = "/static/img/album.png"
    if has_folder_cover:
        cover = "/api/player/albumart"
    elif has_embedded_cover:
        cover = "/api/player/cover"

    # Format duration/elapsed here for UI consistency
    objStatus = mpd.status()
    if objStatus['state'] == "play":
        objStatus['str_duration'] = duration_to_time(objStatus['duration'])
        objStatus['str_elapsed'] = duration_to_time(objStatus['elapsed'])

    return {
        "version": mpd.mpd_version,
        "status": objStatus,
        "stats": mpd.stats(),
        "currentsong": mpd.currentsong(),
        "outputs": mpd.outputs(),
        "cover": cover,
    }

class JukeboxPlayer():

    @staticmethod
    def initialize():
        mpd = get_mpd()

        # Start playing
        mpd.play()   

        return get_status()

    @staticmethod
    def status():
        return get_status()
  
    @staticmethod
    def cover():
        mpd = get_mpd()
        return mpd.readpicture(mpd.currentsong()['file'])
        
    @staticmethod
    def albumart():
        mpd = get_mpd()
        return mpd.albumart(mpd.currentsong()['file'])

    @staticmethod
    def update():
        mpd = get_mpd() 
        ret = mpd.rescan()
        return mpd.status()

    @staticmethod
    def artists():
        return get_mpd().list('artist')

    @staticmethod
    def albums():
        return get_mpd().list('album')

    @staticmethod
    def random():
        mpd = get_mpd()
        random = int(mpd.status()['random'])
        print('random: %s' % random)
        if random == 0: 
            return mpd.random(1)
        else:
            return mpd.random(0)

    @staticmethod
    def repeat():
        mpd = get_mpd()
        repeat = int(mpd.status()['repeat'])
        single = int(mpd.status()['single'])

        # 1 - OFF / OFF - Repeat OFF
        # 2 - ON / OFF  - Repeat ALL
        # 3 - ON / ON   - Repeat ONE

        if repeat == 0 and single == 0:
            mpd.repeat(1)
        elif repeat == 1 and single == 0:
            mpd.single(1)
        else:
            mpd.single(0)
            mpd.repeat(0)
        return True

    @staticmethod
    def mute():
        mpd = get_mpd()
        is_muted = (int(mpd.status()['volume']) == 0)
        if is_muted:
            return mpd.setvol(100)
        else:
            return mpd.setvol(0)

    @staticmethod
    def volume(vol):
        return get_mpd().setvol(vol)

    @staticmethod
    def toggleoutput(oid):
        return get_mpd().toggleoutput(oid)

    @staticmethod
    def seek(s):
        return get_mpd().seekcur(s)

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

    # Playlist
    @staticmethod
    def playlist():
        return get_mpd().playlistinfo()

    @staticmethod
    def playid(song_id):
        return get_mpd().playid(song_id)

    @staticmethod
    def listplaylist(pid):
        return get_mpd().songid(pid)

    @staticmethod
    def playlist_reset(artist):
        mpd = get_mpd()
        mpd.clear()
        mpd.findadd("any", artist)
        mpd.repeat(1)
        mpd.single(0)
        mpd.shuffle()
        mpd.play()