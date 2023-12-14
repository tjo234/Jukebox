echo '''
*** JUKEBOX INSTALLER ***

This will install the latest version of jukebox without overwriting any data.

You should be able to run it over and over again without any issues. 
	'''

# Update Apache Config
apt install apache2

# Replace project code
sudo rm -R /var/www/Jukebox
sudo mkdir /var/www/Jukebox
sudo git clone https://github.com/tjo234/Jukebox.git

# Create/Activate Virtual Environment
cd /var/www/Jukebox
sudo python3 -m venv .env
source .env/bin/activate

# Install dependencies
sudo pip install -r requirements.txt

# Create database/fix ownership
sudo mkdir /var/database
sudo touch /var/database/jukebox.db
sudo chown -R www-data:www-data /var/database
sudo chmod -R u+w /var/database

# Copy Apache Config
sudo cp /var/www/Jukebox/jukebox/server/jukebox.conf /etc/apache2/sites-available/jukebox.conf
sudo a2ensite jukebox

# Reload Apache Server
sudo systemctl reload apache2