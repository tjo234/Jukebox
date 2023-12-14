# Update Apache Config
sudo cp jukebox/server/jukebox.conf /etc/apache2/sites-available/jukebox.conf
sudo a2ensite jukebox
sudo systemctl reload apache2

# Create/Activate Virtual Environment
sudo python3 -m venv .env
source .env/bin/activate

# Install dependencies
sudo pip install -r requirements.txt

# Create database/fix ownership
mkdir /var/database
touch /var/database/jukebox.db
sudo chown -R www-data:www-data /var/database
sudo chmod -R u+w /var/database