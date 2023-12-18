#!/usr/bin/env
import io
from datetime import datetime, timedelta
from flask import Flask, render_template, send_from_directory, send_file, request, jsonify, g

from .database import Database, Track
from .library import Library
from .player import JukeboxPlayer
from. config import ProductionConfig, DevelopmentConfig, TestingConfig

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
    return {
        "genres": GENRES,
        "player": JukeboxPlayer.status()
    }
    
def create_app():
    # Create Flask App
    app = Flask(__name__)
    
    # Load Configuration
    if app.testing:
        app.config.from_object(TestingConfig())
    if app.debug:
        app.config.from_object(DevelopmentConfig())
    else:
        app.config.from_object(ProductionConfig())

    # @app.before_first_request
    # def initialize_db():
    #     # Setup tables if they don't exist
    #     with app.app_context():
    #         Database.initialize()

    @app.teardown_appcontext
    def close_connection(exception):
        Database.close()


    # Root Static Handler (favicon)
    @app.route('/favicon.ico')
    def static_from_root():
        return send_from_directory(app.static_folder, request.path[1:])

    # Page Handler (favicon)
    @app.route('/', defaults={'route': 'index'})
    @app.route('/<route>')
    def render_page(route):
        obj = get_template_values()
        obj['route'] = route
        return render_template('%s.html' % route, **obj) 

    # Partial View Handler
    @app.route('/view/<route>')
    def render_view(route):
        obj = get_template_values()
        return render_template('views/%s.html' % route, **obj)   

    # Player API
    @app.route("/player/status")
    def player_status():
        return jsonify(JukeboxPlayer.status())

    @app.route("/player/update")
    def player_update():
        JukeboxPlayer.update()
        return jsonify(JukeboxPlayer.status())

    @app.route("/player/initialize")
    def player_initialize():
        return jsonify(JukeboxPlayer.initialize())

    @app.route("/player/library")
    def player_library():
        resp = JukeboxPlayer.library()
        return jsonify(resp)

    @app.route("/player/albums")
    def player_library_albums():
        resp = JukeboxPlayer.albums()
        return jsonify(resp)

    @app.route("/player/cover")
    def player_library_cover():
        cover = JukeboxPlayer.cover()
        if cover and 'binary' in cover:
            return send_file(
                io.BytesIO(cover['binary']),
                mimetype=cover['type'],
                as_attachment=False,
                download_name='album.jpg')
        else:
            return "No image found"

    @app.route("/player/artists")
    def player_library_artists():
        resp = JukeboxPlayer.artists()
        return jsonify(resp)

    @app.route("/player/volume/<volume>")
    def player_volume(volume):
        resp = JukeboxPlayer.volume(volume)
        return jsonify(resp)

    @app.route("/player/seek/<seek>")
    def player_seek(seek):
        resp = JukeboxPlayer.seek(seek)
        return jsonify(resp)

    @app.route("/player/control/<control>")
    def player_control(control):
        CONTROLS = ["play", "pause", "stop", "next", "previous", "mute", "random", "repeat"]
        if not control in CONTROLS:
            raise Exception('Control not valid')
        resp = exec("JukeboxPlayer.%s()" % control)
        return jsonify(resp)

    @app.route("/player/listmounts")
    def player_listmounts():
        resp = JukeboxPlayer.listmounts()
        return jsonify(resp)

    @app.route("/player/listneighbors")
    def player_listneighbors():
        resp = JukeboxPlayer.listneighbors()
        return jsonify(resp)

    @app.route("/player/outputs")
    def player_outputs():
        resp = JukeboxPlayer.outputs()
        return jsonify(resp)

    @app.route("/player/idle")
    def player_idle():
        resp = JukeboxPlayer.idle()
        return jsonify(resp)

    # Playlist Handlers
    @app.route("/playlist/<playlist_id>")
    def playlist_playlist_by_id(playlist_id):
        resp = JukeboxPlayer.listplaylist(playlist_id)
        return jsonify(resp)

    @app.route('/playlist')
    def playlist_default():
        resp = JukeboxPlayer.playlist()
        return jsonify(resp)   

    @app.route("/playlist/reset")
    def playlist_playlist_reset():
        resp = JukeboxPlayer.playlist_reset()
        return jsonify(resp)

    # API Handlers (Database)
    @app.route("/api/scan_library")
    def api_scan_library():
        resp = Library.scan_library(app.config['LIBRARY_PATH'])
        return jsonify(resp)

    @app.route("/api/status")
    def api_player_status():
        resp = JukeboxPlayer.status_only()
        return jsonify(resp)

    # @app.route("/api/tracks")
    # def api_get_tracks():
    #     resp = Track.get_tracks()
    #     return jsonify(resp)

    # @app.route("/file/<track_id>")
    # def api_get_file(track_id):
    #     filename = Track.get_track_by_id(track_id)['filename']
    #     return send_file(filename)

   
    # JINJA Template Filters
    @app.template_filter('dt')
    def filter_time_to_date(s):
        return datetime.fromtimestamp(int(s)).strftime('%b %d, %Y %I:%M %p')

    @app.template_filter('seconds')
    def filter_seconds_timedelta(s):
        return timedelta(seconds=int(s))

    @app.template_filter('audio')
    def filter_mpd_audio_str(s):
        audio = s.split(':')
        hz = str(int(audio[0])/1000)
        return hz + ' kHz / ' + audio[1] + ' bit'
        return timedelta(seconds=int(s))
            
    return app