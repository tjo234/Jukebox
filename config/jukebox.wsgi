import os
import sys
import logging

sys.path.insert(0, '/var/www/Jukebox')

os.environ['FLASK_DATABASE'] = 'sql/library.db'

# Set up logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# Import and run the Flask app
from main import app as application