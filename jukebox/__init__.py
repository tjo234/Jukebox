#!/usr/bin/env
from flask import Flask, render_template, send_from_directory, send_file, request, jsonify, g
from .database import Config, Database, Track
from .library import Library

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

def get_template_values():

    tracks = Track.get_tracks()
    albums = Track.get_albums()
    artists = Track.get_artists()
    arrHome = []
    currentTrack = None

    for a in albums:
        track = [t for t in tracks if t['album'] == a[0]][0]
        track['cover'] = Library.get_album_art(track['filename'])
        arrHome.append(track)

    return {
        "settings": Config.fetch(),
        "tracks": tracks,
        "currentTrack": currentTrack,
        "artists": artists,
        "albums": albums,
        "genres": GENRES,
        "home": arrHome
    }

def create_app():
    # Create Flask App
    app = Flask(__name__)
    app.config.from_prefixed_env()

    # Setup tables if they don't exist
    with app.app_context():
        Database.initialize()

    # Static Handlers
    @app.route('/favicon.ico')
    def static_from_root():
        return send_from_directory(app.static_folder, request.path[1:])

    @app.route('/', defaults={'route': 'index'})
    @app.route('/<route>')
    def render_page(route):
        obj = get_template_values()
        obj['route'] = route
        return render_template('%s.html' % route, **obj) 

    @app.route('/view/<route>')
    def render_view(route):
        obj = get_template_values()
        return render_template('views/%s.html' % route, **obj)   

    @app.route("/api/status")
    def api_status():
        resp = {"status": "OK"}
        return jsonify(resp)

    @app.route("/api/scan_library")
    def api_scan_library():
        resp = Library.scan_library()
        return jsonify(resp)

    @app.route("/api/tracks")
    def api_get_tracks():
        resp = Track.get_tracks()
        return jsonify(resp)

    @app.route("/file/<track_id>")
    def api_get_file(track_id):
        filename = Track.get_track_by_id(track_id)['filename']
        return send_file(filename)

    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            print('Closed SQL connection.')
            db.close()
            
    return app