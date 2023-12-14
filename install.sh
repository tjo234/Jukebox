# Install Apache Config
sudo cp config/jukebox.conf /etc/apache2/sites-available/jukebox.conf
sudo a2ensite jukebox
sudo systemctl reload apache2

# Create/Activate Virtual Environment
sudo python3 -m venv .env
source .env/bin/activate

# Install dependencies
pip install -r requirements.txt