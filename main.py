import os 
from jukebox import create_app, listen_for_servers

app = create_app()
app.secret_key = "tM^5^ooYLczLV&Ng"

with app.app_context():
    listen_for_servers()

 # Start the web server
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=9999, debug=True)

    