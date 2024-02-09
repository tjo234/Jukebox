#!/usr/bin/env
import time
from flask import Blueprint, render_template, make_response, send_from_directory, request, g, current_app
from ..player import JukeboxPlayer, MPDServerNotFoundException

view = Blueprint('view', __name__)

def user_on_mobile():
    user_agent = request.headers.get("User-Agent")
    user_agent = user_agent.lower()
    phones = ["android", "iphone"]

    if any(x in user_agent for x in phones):
        return True
    return False

# Root Static Handler (favicon)
@view.route('/favicon.ico')
def static_from_root():
    return send_from_directory(current_app.static_folder, request.path[1:])

# Page Handler (favicon)
@view.route('/', defaults={'route': 'index'})
@view.route('/<route>')
def render_page(route):
    resp = None
    obj = {}
    obj['JUKEBOX_ADDR'] = JukeboxPlayer.addr()
    obj['JUKEBOX_PORT'] = JukeboxPlayer.port()
    try:
        obj['genres'] = JukeboxPlayer.genres()
        obj['player'] = JukeboxPlayer.status()
        obj['outputs'] = JukeboxPlayer.outputs()
        obj['playlists'] = JukeboxPlayer.playlists()
        obj['queue'] = JukeboxPlayer.playlist()
    except MPDServerNotFoundException as ex:
        print(ex)
        pass

    # Append Route and Cookies
    obj['route'] = route  
    obj['now'] = int(time.time() * 1000)

    # Mobile App
    if route == "index" and user_on_mobile():
        obj['device'] = "mobile"  
        resp = render_template('pages/mobile.html', **obj) 

    # Desktop App
    elif route == "index":   
        obj['device'] = "desktop"  
        resp = render_template('pages/desktop.html', **obj) 

    # Static Pages
    else:
        try:
            resp = render_template('pages/%s.html' % route, **obj) 
        except:
            resp = render_template('pages/404.html', **obj) 

    # Set Cookie
    # resp = make_response(resp) 
    # resp.set_cookie('JUKEBOX_ADDR', JukeboxPlayer.addr())
    # resp.set_cookie('JUKEBOX_PORT', str(JukeboxPlayer.port()))
    return resp

# Partial View Handler
@view.route('/view/<route>')
def render_desktop_view(route):
    obj = {} 
    obj['route'] = route
    obj['JUKEBOX_ADDR'] = JukeboxPlayer.addr()
    obj['JUKEBOX_PORT'] = JukeboxPlayer.port()
    try:
        obj['player'] = JukeboxPlayer.status()
        obj['stats'] = JukeboxPlayer.stats()

        if route == "home":
            obj['home'] = JukeboxPlayer.albums()[:6]
            obj['playlists'] = JukeboxPlayer.playlists()

        if route == "browse":
            path = request.args.get('path', '')
            obj['path'] = path
            obj['parent'] = ("/".join(path.rsplit("/")[:-1])) if '/' in path else ''
            obj['browse'] = JukeboxPlayer.browse(path)

        if route in ["queue", "queue-simple"]:
            obj['queue'] = JukeboxPlayer.playlist()

        if route == "albums":
            album = request.args.get('album', None)
            artist = request.args.get('artist', None)
            
            if album:
                obj['album'] = album
                obj['album_tracks'] = JukeboxPlayer.album(album)
            elif artist:
                obj['artist'] = artist
                obj['albums'] = JukeboxPlayer.albums(artist)
            else:
                obj['albums'] = JukeboxPlayer.albums()

        if route == "artists":
            obj['artists'] = JukeboxPlayer.artists()

        if route == "radio":
            obj['genres'] = JukeboxPlayer.genres()

        if route == "artists":
            obj['artists'] = JukeboxPlayer.artists()

        if route == "playlists":
            obj['playlists'] = JukeboxPlayer.playlists()

        if route == "playlist":
            playlist = request.args.get('playlist', None)
            obj['playlist'] = playlist
            obj['playlist_tracks'] = JukeboxPlayer.playlistinfo(playlist)

    except MPDServerNotFoundException:
        pass
       
    return render_template('views/%s.html' % route, **obj) 
