#!/usr/bin/env
from flask import Blueprint, jsonify, send_file, request

from ..player import JukeboxPlayer

api = Blueprint('api', __name__, url_prefix='/api')

@api.route("/status")
def api_status():
    return "OK"
    
# Player API
@api.route("/player/status")
def player_status():
    return jsonify(JukeboxPlayer.status())

@api.route("/player/ping")
def player_ping():
    return jsonify(JukeboxPlayer.ping())

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

@api.route('/playlist/load/')
def playlist_load_playlist():
    playlist = request.args.get('playlist')
    resp = JukeboxPlayer.load(playlist=playlist)
    return jsonify(resp)  

@api.route('/playlist/track/')
def playlist_load_playlist_track():
    playlist = request.args.get('playlist')
    track = request.args.get('track')
    resp = JukeboxPlayer.playlist_track(playlist, track)
    return jsonify(resp)   

@api.route("/playlist/queue/artist/")
def playlist_play_artist():
    artist = request.args.get('artist')
    resp = JukeboxPlayer.playlist_play_artist(artist)
    return jsonify(resp)

@api.route("/playlist/queue/album/")
def playlist_play_album():
    album = request.args.get('album')
    resp = JukeboxPlayer.playlist_play_album(album)
    return jsonify(resp)

@api.route("/album/play/")
def playlist_play_album_track():
    album = request.args.get('album')
    track = request.args.get('track')
    resp = JukeboxPlayer.playlist_play_album_track(album, track)
    return jsonify(resp)

@api.route("/playlist/findadd/<tag>/<what>")
def playlist_playlist_findadd(tag, what):
    resp = JukeboxPlayer.findadd(tag, what)
    return jsonify(resp)

@api.route("/playlist/add/")
def playlist_playlist_add():
    file = request.args.get('file')
    resp = JukeboxPlayer.add(file)
    return jsonify(resp)

@api.route("/playlist/save/")
def playlist_playlist_save():
    playlist = request.args.get('playlist')
    resp = JukeboxPlayer.save(playlist)
    return jsonify(resp)

@api.route("/playlist/clear/")
def playlist_playlist_clear():
    resp = JukeboxPlayer.clear()
    return jsonify(resp)

# SONG_ID
@api.route("/playlist/playid/<song_id>")
def playlist_playlist_by_song_id(song_id):
    resp = JukeboxPlayer.playid(song_id)
    return jsonify(resp)

# SONG_ID
@api.route("/playlist/deleteid/<song_id>")
def playlist_delete_by_song_id(song_id):
    resp = JukeboxPlayer.deleteid(song_id)
    return jsonify(resp)

@api.route("/cover/")
@api.route("/cover/<song_id>")
@api.route("/album/")
@api.route("/album/<path:file>")
def player_library_cover(song_id=None, file=None):
    cover = JukeboxPlayer.cover(song_id=song_id, file=file)
    return send_file(cover, download_name="%s.jpg" % song_id)

@api.route("/search/<s>")
def api_search(s):
    resp = JukeboxPlayer.search(s)
    return jsonify(resp)

@api.route("/cache_album_covers")
def api_cache_album_covers():
    resp = JukeboxPlayer.cache_album_covers(skip_existing=True)
    return jsonify(resp)

@api.route("/recache_album_covers")
def api_recache_album_covers():
    resp = JukeboxPlayer.cache_album_covers(skip_existing=False)
    return jsonify(resp)
