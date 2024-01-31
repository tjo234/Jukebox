#!/usr/bin/env
import io
import os
import base64
import socket
import urllib

from mpd import MPDClient, CommandError
from flask import g, request
from socket import gaierror

from .utils import *

ALBUM_CACHE_PATH = "jukebox/static/img/albums/"
ALBUM_PATH = "jukebox/static/img/album.jpg"

JUKEBOX_DEFAULT_ADDR = "jukebox.local"
JUKEBOX_DEFAULT_PORT = 6600

class MPDServerNotFoundException(Exception):
    pass

def get_connection():
    # Connect to MPD
    mpd = MPDClient()
    addr = JukeboxPlayer.addr()
    port = JukeboxPlayer.port()
    try:    
        mpd.connect(addr, port)
        g._mpd = mpd
    except:
        s = "Could not locate the server at %s:%s" % (addr,port)
        raise MPDServerNotFoundException(s)
    return g._mpd

def get_mpd():
    mpd = getattr(g, '_mpd', None)
    if not mpd:    
       mpd = get_connection()
    return mpd


def cache_album_cover(album_name, skip_existing=True):
    
    # Check for blank
    if not album_name or album_name == "":
        return

    # Get path
    img_path = ALBUM_CACHE_PATH + "%s.jpg" % urllib.parse.quote_plus(album_name)

    # Check if image exists
    if os.path.exists(img_path) and skip_existing == True:
        return 

    # Find track by album
    mpd = get_mpd()
    file = mpd.find('album', album_name)[0]['file']

    # Get embedded image
    img_bytes = None
    try:
        img_bytes = mpd.readpicture(file)['binary']
    except:
        pass

    # Get folder image
    if img_bytes == None:
        try:
            img_bytes = mpd.albumart(file)['binary']
        except:
            pass

    # Add Default Image
    if not img_bytes:
        print("No image found for: %s" % album_name)

        # Load default image
        with open(ALBUM_PATH, "rb") as f:
            img_bytes = f.read()

    # Write album to cache folder
    with open(img_path, "wb") as binary_file:
        binary_file.write(img_bytes)
        print("Cached image for: %s" % album_name)
 
class JukeboxPlayer():

    @staticmethod
    def status():
        mpd = get_mpd()

        # Format duration/elapsed for UI consistency
        status = mpd.status()
        if status['state'] == "play":
            status['str_duration'] = duration_to_time(status['duration'])
            status['str_elapsed'] = duration_to_time(status['elapsed'])
            status['audio_hz'] = mpd_audio_hz(status['audio'])
            status['audio_bits'] = mpd_audio_bits(status['audio'])
        return {
            "status": status,
            "currentsong": mpd.currentsong(),
            "version": mpd.mpd_version
        }   

    @staticmethod
    def version():
        return get_mpd().mpd_version

    @staticmethod
    def addr():
        return request.cookies.get('JUKEBOX_ADDR', JUKEBOX_DEFAULT_ADDR) 

    @staticmethod
    def port():
        return request.cookies.get('JUKEBOX_PORT', JUKEBOX_DEFAULT_PORT) 

    @staticmethod
    def browse(path):
        print(path)
        return get_mpd().lsinfo(path)

    @staticmethod
    def stats():
        return get_mpd().stats()
  
    @staticmethod
    def cover(song_id=None, file=None):
        mpd = get_mpd()

        # Load by Filename
        if file:
            file = urllib.parse.unquote(file)
    
        # Load by ID
        if song_id:
            file = mpd.playlistid(song_id)[0]['file']

        print ("File: %s" % file)

        # Load album.jpg from folder
        try:
            cover = mpd.albumart(file)['binary']
            return io.BytesIO(cover)
        except:
            pass

        # Load embedded ID3 album
        try:
            cover = mpd.readpicture(file)['binary']
            return io.BytesIO(cover)
        except:
            pass

        # Default Album
        f = open(ALBUM_PATH, "rb")
        return io.BytesIO(f.read())

    @staticmethod
    def cache_album_covers(skip_existing=True):
        # Get albums        
        albums = get_mpd().list('album', 'group', 'albumartist')[1:]
        success = 0
        fail = 0
        for a in [a['album'] for a in albums]:
            try:
                cache_album_cover(album_name=a, skip_existing=skip_existing)
                success += 1
            except Exception as ex:
                fail += 1
                print("ERROR caching image for: %s" % a)
                print(ex)
        return "Success: %s, Fail: %s" % (str(success), str(fail))
        
    @staticmethod
    def database_update(rescan=False):
        mpd = get_mpd() 
        if rescan:
            return mpd.rescan()
        else:
            return mpd.update()

    @staticmethod
    def artists():
        return get_mpd().list('albumartist')[1:]

    @staticmethod
    def genres():
        return get_mpd().list('genre')

    @staticmethod
    def albums():
        mpd = get_mpd()
        albums = mpd.list('album', 'group', 'albumartist')[1:]
        return albums

    @staticmethod
    def albums_home():
        mpd = get_mpd()
        albums = mpd.list('album', 'group', 'albumartist')[1:7]
        for a in albums:
            try:
                a['image'] = '/api/album/' + urllib.parse.quote(mpd.find('album', a['album'])[0]['file'])
            except:
                pass
        return albums

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
    def add(file):
        mpd = get_mpd()
        mpd.add(file)
        mpd.play()

    @staticmethod
    def save(name):
        return get_mpd().save(name)

    @staticmethod
    def clear():
        return get_mpd().clear()

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
    def idle(signal=None):
        if signal:
            return get_mpd().idle(signal)
        else:
            return get_mpd().idle()

    @staticmethod
    def outputs():
        return get_mpd().outputs()

    @staticmethod
    def search(search):
        mpd = get_mpd()
        return {
            'artists': [a['albumartist'] for a in g.artists if a['albumartist'].find(search) == 0],
            'albums': [a['album'] for a in g.albums if a['album'].find(search) == 0],
            'tracks': mpd.search("any", search)
        }

    # Playlist
    @staticmethod
    def playlist():
        return get_mpd().playlistinfo()

    @staticmethod
    def playlists():
        return get_mpd().listplaylists()

    @staticmethod
    def load(playlist):
        print('Loading playlist: %s' % playlist)
        mpd = get_mpd()
        mpd.clear()
        mpd.load(playlist)
        mpd.repeat(1)
        mpd.single(0)
        mpd.random(0)
        mpd.play()

    @staticmethod
    def playid(song_id):
        return get_mpd().playid(song_id)

    @staticmethod
    def deleteid(song_id):
        return get_mpd().deleteid(song_id)

    @staticmethod
    def listplaylist(pid):
        return get_mpd().songid(pid)

    @staticmethod
    def findadd(tag, what):
        mpd = get_mpd()
        mpd.clear()
        mpd.findadd(tag, what)
        mpd.repeat(1)
        mpd.single(0)
        mpd.random(0)
        mpd.shuffle()
        mpd.play()

    @staticmethod
    def album(album):
        mpd = get_mpd()
        return mpd.find("album", album)

    @staticmethod
    def playlist_play_album(album):
        mpd = get_mpd()
        mpd.clear()
        mpd.findadd("album", album)
        mpd.repeat(1)
        mpd.single(0)
        mpd.random(0)
        mpd.play()

    @staticmethod
    def playlist_play_album_track(album, track):
        mpd = get_mpd()
        mpd.clear()
        mpd.findadd("album", album)
        mpd.repeat(1)
        mpd.single(0)
        mpd.random(0)
        mpd.play(track)

    @staticmethod
    def playlist_play_artist(artist):
        mpd = get_mpd()
        mpd.clear()
        mpd.findadd("artist", artist)
        mpd.repeat(1)
        mpd.single(0)
        mpd.random(1)
        mpd.play()