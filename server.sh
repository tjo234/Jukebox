echo '''
*** JUKEBOX INSTALLER ***

This will install the latest version of jukebox without overwriting any data.

You should be able to run it over and over again without any issues. 
	'''

# Install Apache Web Server
apt install apache2

# Install Music Player Daemon
apt install mpd

# Delete/replace application folder
sudo rm -R /var/www/Jukebox

# Download latest application code
sudo git clone https://github.com/tjo234/Jukebox.git

# Create VirtualEnv
cd /var/www/Jukebox
sudo python3 -m venv .env
source .env/bin/activate

# Install dependencies into VirtualEnv
sudo pip install -r requirements.txt

# Create database 
sudo mkdir /var/database
sudo touch /var/database/jukebox.db

# Fix DB permissions (www-data is Apache user)
sudo chown -R www-data:www-data /var/database
sudo chmod -R u+w /var/database

# Replace Apache Config file
sudo cp /var/www/Jukebox/jukebox/server/jukebox.conf /etc/apache2/sites-available/jukebox.conf
sudo a2ensite jukebox

# Reload Apache Server
sudo systemctl reload apache2