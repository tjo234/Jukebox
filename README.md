# Jukebox
Jukebox is a free and open source Hi-Fi music player. 

## What is Jukebox? 
Jukebox is a media server for hi-res audio. 

## What you'll need:
- RaspberryPi (v3/v4)
- External Hard Drive (SSD recommended)

# How does it work?

## 1. Install Jukebox

Run the installer script from terminal:
`wget -O - https://raw.githubusercontent.com/tjo234/Jukebox/main/scripts/install.sh | bash`

This will update your system, install Jukebox, and launch the server.

## 2. Launch the Jukebox App

- On the RaspberryPi, visit `http://localhost/`
- On another computer on the same Wifi network, visit `http://jukebox.local/`

You should see the Jukebox App loaded up, with a test file playing.

## 3. Load Your Music

We recommend keeping your music on an external SSD drive:

- Plug in a hard-drive named `MUSIC` (Jukebox will automatically recognize it)
- Create a symbolic link to your external drive in the MPD server directory `/var/mpd/music/`

Make sure you your music is properly ID3 tagged. Ideally in a high-resolution format (FLAC). 

You can also use a tool like Musicbrainz Picard to make sure your album art is updated.

NOTE: You can also copy your music directly to the SD card in `/var/mpd/music/` but we don't recommend it.

**Why not? SD cards are more likely to fail in the long term. You don't want to lose your precious music!

It is also much faster to get Jukebox up and running again.

## 4. Refresh the Library 

Goto 'Settings' in the bottom left and click 'Rescan Library'.

You'll see a loading indicator. When it finishes go back into settings and click 'Refresh App'.

You should now see music in the Album/Artist/Browse section.

## 5. Start Listening!

Plug in your headphones, or connect your Jukebox to your stereo receiver.

You can also use the HDMI port to see a "Now Playing" screen on your TV.

NOTE: There is no audio sent over the HDMI port, only the Now Playing screen. 


-------

# Install Jukebox Server
`wget -O - https://raw.githubusercontent.com/tjo234/Jukebox/main/scripts/install.sh | bash`

# Update Jukebox Server
`wget -O - https://raw.githubusercontent.com/tjo234/Jukebox/main/scripts/update.sh | bash`