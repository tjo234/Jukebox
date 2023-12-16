#!/usr/bin/env
import base64
import os
import mutagen

from io import BytesIO
from mutagen.easyid3 import EasyID3
from PIL import Image

from .database import Track
from .utils import convert_size

EXTENSIONS = [".mp3", ".flac", ".wav"]

class Library():
    @staticmethod
    def scan_library(Library_path):
        count = 0
        size_bytes = 0
        arrInsert = []
        arrUpdate = []

        print(Library_path)

        # Loop through DB entries, look for missing physical files
        rows_deleted = 0
        for t in Track.get_tracks():
            filename = t['filename']
            if not os.path.exists(filename):          
                Track.delete(filename)
                rows_deleted += 1

        # Loop through physical files, look for new DB entries
        for folder, subs, files in os.walk(Library_path):
            for file in files:
                # Exclude DB file and hidden files
                ext = os.path.splitext(file)[1]
                print("extension", ext)
                if file.find('.') != 0 and ext in EXTENSIONS:
                    count += 1
                    filename = os.path.join(Library_path, folder, file)
                    size_bytes += os.path.getsize(filename)

                    # Check for existing DB record
                    track = Track.get_track_by_path(filename)
                    if not track:
                        obj = get_track_object(filename)
                        if obj:
                            arrInsert.append(obj)
                    
        # Insert rows into SQL database
        rows_inserted = Track.create(arrInsert)

        return {
            "count": count,
            "size": convert_size(size_bytes),
            "rows_inserted": rows_inserted,
            "rows_deleted": rows_deleted,
        }
    
    @staticmethod
    def get_album_art(filename):
        try:
            tags = mutagen.File(filename)
            img_base64 = base64.b64encode(tags.get("APIC:").data).decode("utf-8")
            img_mime = tags.get("APIC:").mime
            return "data:%s;base64,%s" % (img_mime, img_base64)
        except:
            return "/static/img/album.png"
                
def get_track_object(filename):
    id3 = EasyID3(filename)
    keys = id3.keys() 

    title = id3.get("title")[0] if "title" in keys else None
    artist = id3.get("artist")[0] if "artist" in keys else None
    albumartist = id3.get("albumartist")[0] if "albumartist" in keys else None
    album = id3.get("album")[0] if "album" in keys else None
    genre = id3.get("genre")[0] if "genre" in keys else None
    year = id3.get("date")[0] if "date" in keys else None
    tracknumber = id3.get("tracknumber")[0] if "tracknumber" in keys else None
    discnumber = id3.get("discnumber")[0] if "discnumber" in keys else None

    return {
        "filename": filename,
        "track": title,
        "artist": artist,
        "albumartist": albumartist,
        "album": album,
        "genre": genre,
        "year": year,
        "tracknumber": tracknumber,
        "discnumber": discnumber
    }