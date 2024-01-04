# Developer Notes
How to run and debug the Flask application locally.

## These instructions are for people looking to run/debug the Flask web server code. 

If you are simply looking to run Jukebox, check out README.

# Setup 
- Run `dev.sh` to create the Virtual Environment and start the web server

# Running the App 
- Run `dev.sh` to start the web server

# Testing
- Run unittests `python3 -m unittest discover -v`


-------

# Server Installation

Copy following into terminal on your RaspberryPi (v3/v4) to install Jukebox Server:

# Install Jukebox Server
`wget -O - https://raw.githubusercontent.com/tjo234/Jukebox/main/scripts/install.sh | bash`

# Update Jukebox Server
`wget -O - https://raw.githubusercontent.com/tjo234/Jukebox/main/scripts/update.sh | bash`