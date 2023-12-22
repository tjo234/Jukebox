#!/usr/bin/env
from flask import Blueprint, render_template, send_from_directory, request, g, current_app

from ..player import JukeboxPlayer


view = Blueprint('view', __name__)

GENRES = [
    {
        "name": "Grateful Dead",
        "image": "dead.png"
    },
    {
        "name": "Hip-Hop/Rap",
        "image": "hiphop.png"
    },
     {
        "name": "Electronica",
        "image": "electronica.png"
    },
    {
        "name": "Rock & Roll",
        "image": "rock.png"
    },
    {
        "name": "R&B/Soul",
        "image": "soul.png"
    },
    {
        "name": "Blues",
        "image": "blues.png"
    },
    {
        "name": "Folk/Acoustic",
        "image": "folk.png"
    },
]

def user_on_mobile():
    user_agent = request.headers.get("User-Agent")
    user_agent = user_agent.lower()
    phones = ["android", "iphone"]

    if any(x in user_agent for x in phones):
        return True
    return False

def get_template_values():
    return {
        "genres": GENRES,
        "player": JukeboxPlayer.status(),
        "playlist": JukeboxPlayer.playlist()
    }

# Root Static Handler (favicon)
@view.route('/favicon.ico')
def static_from_root():
    return send_from_directory(current_app.static_folder, request.path[1:])

# Page Handler (favicon)
@view.route('/', defaults={'route': 'index'})
@view.route('/<route>')
def render_page(route):
    obj = get_template_values()
    obj['route'] = route
    if user_on_mobile():
        print('Mobile User')
        return render_template('mobile/index.html', **obj) 
    else:
        try:
            return render_template('pages/%s.html' % route, **obj) 
        except:
            return render_template('pages/404.html', **obj) 

# Partial View Handler
@view.route('/view/<route>')
def render_view(route):
    obj = get_template_values()
    return render_template('views/%s.html' % route, **obj)   
