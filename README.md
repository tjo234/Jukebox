# Jukebox
Jukebox is a free and open source Hi-Fi music player.

## What is Jukebox? 
Jukebox is a media server for hi-res audio.

## How does it work?
1. Install Jukebox on a Wi-Fi enabled RaspberryPi (or any computer)
2. Upload your music (properly ID3 tagged in high-resolution FLAC format)
3. Connect your Jukebox server into your TV or stereo system 
4. Open the Jukebox Remote app on your phone or web browser
5. Listen to the music play!

------

# Set up a development environment

1. Clone the repo
2. Run `python3 -m venv env` to create a python virtual environment
3. Activate the virtual environment by `source env/bin/activate`
4. Run `pip install -r requirements.txt` to install required packages (into the virtual environment)

Development Server:
- Activate the virtual environment by `source env/bin/activate`
- Run the development server: `python3 main.py`
- Visit localhost in the browser: `http://localhost:9999/`

# Testing

1. Run unittests `python3 -m unittest discover -v`

-------

# Install Jukebox Server
`wget -O - https://raw.githubusercontent.com/tjo234/Jukebox/main/setup/install.sh | bash`


