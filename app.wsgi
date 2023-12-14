import sys
import logging
 
sys.path.insert(0, '/var/www/Jukebox')
sys.path.insert(0, '/var/www/Jukebox/env/lib/python3.11/site-packages/')
 
# Set up logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
 
# Import and run the Flask app
from main import app as application