import os 
from jukebox import create_app

app = create_app()

 # Start the web server
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=9999, debug=True)