# Jukebox
Jukebox is a free and open source Hi-Fi music player.

Take an inexpensive, silent and low-consumption mini-PC and turn it into a music server/player.

Your music plays from the Jukebox device while you control playlist and volume from your phone/tablet.  
 
## Why Jukebox?
I wanted a portable device that I could store my music on. Many music servers exist, but they usually run on a laptop or full-sized PC. With storage becoming so cheap, I wanted something that I could plug in and start listerning without all the hassle of connect to WiFi or logging into an account. 

## What is it? 
It's basically an iPod that plays FLAC (hi-res audio) files. 

If you goto a party and the host doesn't have internet, just plug this bad boy into TV/speakers and everyone can add music to the playlist.

## Why not just listen to Spotify?
How will you listen to music when the zombie apocalyse hits?

## What is Jukebox
Jukebox gives you the same experience as Spotify or iTunes without all the overhead.

## How does it work?
1. Turn on Jukebox and connec to WiFi
2. Connect it to your speakers or TV
3. Upload your music (ideally in FLAC format)
4. Start grooving!

------

# Set up a development environment

1. Clone the repo
2. Run `python -m venv env` to create a python virtual environment
3. Activate the virtual environment by `source env/bin/activate`
4. Run `pip install -r requirements.txt` to install required packages (into the virtual environment)

Development Server:
- Activate the virtual environment by `source env/bin/activate`
- Run the development server: `python3 main.py`
- Visit localhost in the browser: `http://localhost:9999/`

# Testing

1. Run unittests `python3 -m unittest discover -v`
