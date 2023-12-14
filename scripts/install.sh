# Export environment variables
export FLASK_DATABASE="sql/library.db"

# Install Apache Config
sudo cp jukebox.conf /etc/apache2/sites-available/jukebox.conf
sudo a2ensite jukebox
systemctl reload apache2

# Create/Activate Virtual Environment
python3 -m venv .env
source .env/bin/activate

# Install dependencies
pip install -r requirements.txt