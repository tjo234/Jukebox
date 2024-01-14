#!/usr/bin/env
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

def get_template_values():
    return {
        "genres": JukeboxPlayer.genres(),
        "player": JukeboxPlayer.status(),
        "playlist": JukeboxPlayer.playlist(),
        "playlists": JukeboxPlayer.playlists(),
        "outputs": JukeboxPlayer.outputs(),
    }

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

    # Load Server Status
    try:
        obj = get_template_values() 
        if route == "index":   
            obj['home'] = JukeboxPlayer.albums_home()
            obj['artists'] = JukeboxPlayer.artists()
            obj['albums'] = JukeboxPlayer.albums()
    except MPDServerNotFoundException:
        pass

    # Append Route and Cookies
    obj['route'] = route  
    obj['JUKEBOX_ADDR'] = JukeboxPlayer.addr()
    obj['JUKEBOX_PORT'] = JukeboxPlayer.port()

    # Mobile App
    if route == "index" and user_on_mobile():
        obj['device'] = "mobile"  
        resp = render_template('mobile/app.html', **obj) 

    # Desktop App
    elif route == "index":   
        obj['device'] = "desktop"  
        resp = render_template('desktop/app.html', **obj) 

    # Static Pages
    else:
        try:
            resp = render_template('pages/%s.html' % route, **obj) 
        except:
            resp = render_template('pages/404.html', **obj) 

    # Set Cookie
    resp = make_response(resp) 
    resp.set_cookie('JUKEBOX_ADDR', JukeboxPlayer.addr())
    resp.set_cookie('JUKEBOX_PORT', str(JukeboxPlayer.port()))
    return resp

# Partial View Handler
@view.route('/view/desktop/<route>')
def render_desktop_view(route):
    obj = {} 
    obj['route'] = route
    obj['JUKEBOX_ADDR'] = JukeboxPlayer.addr()
    obj['JUKEBOX_PORT'] = JukeboxPlayer.port()
    try:
        obj['player'] = JukeboxPlayer.status()
        obj['stats'] = JukeboxPlayer.stats()
        if route == "browse":
            path = request.args.get('path', '')
            obj['path'] = path
            obj['parent'] = path.rsplit('/')[0] if '/' in path else ''
            obj['browse'] = JukeboxPlayer.browse(path)
        if route == "queue":
            obj['playlist'] = JukeboxPlayer.playlist()
        if route == "albums":
            obj['albums'] = JukeboxPlayer.artists()
        if route == "artists":
            obj['artists'] = JukeboxPlayer.artists()
    except MPDServerNotFoundException:
        pass
       
    return render_template('desktop/views/%s.html' % route, **obj) 

# Partial View Handler
@view.route('/view/mobile/<route>')
def render_mobile_view(route):
    obj = {} 
    obj['route'] = route
    obj['JUKEBOX_ADDR'] = JukeboxPlayer.addr()
    obj['JUKEBOX_PORT'] = JukeboxPlayer.port()
    if route == "radio":
        obj['genres'] = JukeboxPlayer.genres()
    elif route in ["queue"]:
        obj['player'] = JukeboxPlayer.status()
        obj['playlist'] = JukeboxPlayer.playlist()
    
    return render_template('mobile/views/%s.html' % route, **obj)   
