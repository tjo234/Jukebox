#!/usr/bin/env
import math
from datetime import timedelta

def duration_to_time(s):
    arr = str(timedelta(seconds=float(s))).split(':')
    if int(arr[0]) != 0:
        return arr[0] + ':' + arr[1] + ':' + arr[2].split('.')[0]
    else:
        return arr[1] + ':' + arr[2].split('.')[0]

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    
    return "%s %s" % (s, size_name[i])