#!/usr/bin/env
from flask import Blueprint, jsonify, send_file

from ..player import JukeboxPlayer

api = Blueprint('api', __name__, url_prefix='/api')

# Player API
@api.route("/player/status")
def player_status():
    return jsonify(JukeboxPlayer.status())

@api.route("/player/update")
def player_update():
    return jsonify(JukeboxPlayer.database_update())

@api.route("/player/rescan")
def player_rescan():
    return jsonify(JukeboxPlayer.database_update(True))

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
@api.route("/player/idle/<signal>")
def player_idle(signal=None):
    resp = JukeboxPlayer.idle(signal)
    return jsonify(resp)

# Playlist Handlers
@api.route("/playlist/<playlist_id>")
def playlist_playlist_by_id(playlist_id):
    resp = JukeboxPlayer.listplaylist(playlist_id)
    return jsonify(resp)

@api.route('/playlist')
def playlist_default():
    resp = JukeboxPlayer.playlist()
    return jsonify(resp)   

@api.route('/playlists')
def playlist_list_playlists():
    resp = JukeboxPlayer.playlists()
    return jsonify(resp)   

@api.route('/playlist/load/<name>')
def playlist_load_playlist(name):
    resp = JukeboxPlayer.load(name)
    return jsonify(resp)   

@api.route("/playlist/queue/artist/<artist>")
def playlist_play_artist(artist):
    resp = JukeboxPlayer.playlist_play_artist(artist)
    return jsonify(resp)

@api.route("/playlist/queue/album/<album>")
def playlist_play_album(album):
    resp = JukeboxPlayer.playlist_play_album(album)
    return jsonify(resp)

@api.route("/playlist/findadd/<tag>/<what>")
def playlist_playlist_findadd(tag, what):
    resp = JukeboxPlayer.findadd(tag, what)
    return jsonify(resp)

# SONG_ID
@api.route("/playlist/playid/<song_id>")
def playlist_playlist_by_song_id(song_id):
    resp = JukeboxPlayer.playid(song_id)
    return jsonify(resp)

@api.route("/cover/")
@api.route("/cover/<song_id>")
@api.route("/album/<path:file>")
def player_library_cover(song_id=None, file=None):
    cover = JukeboxPlayer.cover(song_id=song_id, file=file)
    return send_file(cover, download_name="%s.jpg" % song_id)

@api.route("/search/<s>")
def api_search(s):
    resp = JukeboxPlayer.search(s)
    return jsonify(resp)

@api.route("/status")
def api_status():
    return "OK"
