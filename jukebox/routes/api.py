#!/usr/bin/env
import io
from flask import Blueprint, jsonify, send_file

from ..player import JukeboxPlayer

api = Blueprint('api', __name__, url_prefix='/api')

@api.route("/status")
def api_status():
	return "OK"

# Player API
@api.route("/player/status")
def player_status():
    return jsonify(JukeboxPlayer.status())

@api.route("/player/update")
def player_update():
    return jsonify(JukeboxPlayer.update())

@api.route("/player/initialize")
def player_initialize():
    return jsonify(JukeboxPlayer.initialize())

@api.route("/player/library")
def player_library():
    resp = JukeboxPlayer.library()
    return jsonify(resp)

@api.route("/player/albums")
def player_library_albums():
    resp = JukeboxPlayer.albums()
    return jsonify(resp)

@api.route("/player/cover")
def player_library_cover():
    try:
        cover = JukeboxPlayer.cover()
        return send_file(io.BytesIO(cover['binary']), mimetype=cover['type'])
    except Exception as ex:
        return str(ex)

@api.route("/player/albumart")
def player_library_albumart():
    try:
        albumart = JukeboxPlayer.albumart()
        return send_file(io.BytesIO(albumart['binary']), download_name="album.jpg")
    except Exception as ex:
        return str(ex)      

@api.route("/player/artists")
def player_library_artists():
    resp = JukeboxPlayer.artists()
    return jsonify(resp)

@api.route("/player/volume/<volume>")
def player_volume(volume):
    resp = JukeboxPlayer.volume(volume)
    return jsonify(resp)

@api.route("/player/seek/<seek>")
def player_seek(seek):
    resp = JukeboxPlayer.seek(seek)
    return jsonify(resp)

@api.route("/player/control/<control>")
def player_control(control):
    CONTROLS = ["play", "pause", "stop", "next", "previous", "mute", "random", "repeat"]
    if not control in CONTROLS:
        raise Exception('Control not valid')
    resp = exec("JukeboxPlayer.%s()" % control)
    return jsonify(resp)

@api.route("/player/outputs")
def player_outputs():
    resp = JukeboxPlayer.outputs()
    return jsonify(resp)

@api.route("/player/toggleoutput/<oid>")
def player_toggleoutput(oid):
    resp = JukeboxPlayer.toggleoutput(oid)
    return jsonify(resp)

@api.route("/player/idle")
def player_idle():
    resp = JukeboxPlayer.idle()
    return jsonify(resp)

# Playlist Handlers
@api.route("/playlist/<playlist_id>")
def playlist_playlist_by_id(playlist_id):
    resp = JukeboxPlayer.listplaylist(playlist_id)
    return jsonify(resp)

# Playlist Handlers
@api.route("/playlist/playid/<song_id>")
def playlist_playlist_by_song_id(song_id):
    resp = JukeboxPlayer.playid(song_id)
    return jsonify(resp)

@api.route('/playlist')
def playlist_default():
    resp = JukeboxPlayer.playlist()
    return jsonify(resp)   

@api.route("/playlist/reset/<artist>")
def playlist_playlist_reset(artist):
    resp = JukeboxPlayer.playlist_reset(artist)
    return jsonify(resp)