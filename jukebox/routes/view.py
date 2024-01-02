#!/usr/bin/env
from flask import Blueprint, render_template, send_from_directory, request, g, current_app
from ..player import JukeboxPlayer

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
    obj = {}
    obj = get_template_values() 
    if not obj:
        obj['connected'] = False    
    obj['route'] = route  

    if route == "index" and user_on_mobile():
        obj['device'] = "mobile"  
        
        return render_template('mobile/app.html', **obj) 
    
    if route == "index":   
        obj['device'] = "desktop"  
        obj['home'] = JukeboxPlayer.albums_home()
        obj['artists'] = JukeboxPlayer.artists()
        obj['albums'] = JukeboxPlayer.albums()
        return render_template('desktop/app.html', **obj) 

    try:
        print('Page: ' + route)
        return render_template('pages/%s.html' % route, **obj) 
    except:
        return render_template('pages/404.html', **obj) 

# Partial View Handler
@view.route('/view/desktop/<route>')
def render_desktop_view(route):
    obj = {} 
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
    
    
    return render_template('desktop/views/%s.html' % route, **obj) 

# Partial View Handler
@view.route('/view/mobile/<route>')
def render_mobile_view(route):
    obj = {} 
    if route == "radio":
        obj['genres'] = JukeboxPlayer.genres()
    elif route in ["queue"]:
        obj['player'] = JukeboxPlayer.status()
        obj['playlist'] = JukeboxPlayer.playlist()
    
    return render_template('mobile/views/%s.html' % route, **obj)   
