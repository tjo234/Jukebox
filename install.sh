# Install Apache Config
sudo cp config/jukebox.conf /etc/apache2/sites-available/jukebox.conf
sudo a2ensite jukebox
sudo systemctl reload apache2

# Create/Activate Virtual Environment
sudo python3 -m venv .env
source .env/bin/activate

# Install dependencies
sudo pip install -r requirements.txt


# Create database/fix ownership
mkdir sql
touch sql/library.db
sudo chown -R www-data:www-data sql
sudo chmod -R u+w sql