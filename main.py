#!/usr/bin/env
from flask import Flask, render_template, send_from_directory, request, jsonify
from jukebox import Database, Config, Track, Library

def get_template_values():
    tracks = Track.get_tracks()
    albums = Track.get_albums()
    arrHome = []
    for a in albums:
        track = [t for t in tracks if t['album'] == a[0]][0]
        track['cover'] = Library.get_album_art(track['filename'])
        arrHome.append(track)

    return {
        "settings": Config.fetch(),
        "tracks": tracks,
        "artists": Track.get_artists(),
        "albums": albums,
        "genres": Track.get_genres(),
        "home": arrHome
    }

# Create Flask App
app = Flask(__name__)

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
def api_get_files():
    resp = Track.get_tracks()
    return jsonify(resp)

if __name__ == "__main__":

    # Run the web server
    app.run(host="127.0.0.1", port=9999, debug=True)