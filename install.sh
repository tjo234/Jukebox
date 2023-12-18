echo '''
*** JUKEBOX INSTALLER ***

This will install the latest version of jukebox and its dependencies.

You should be able to run it multiple times without any issue. 

'''

# Update APT to latest version

print('JUKEBOX - Update APT installer to latest version...')
sudo apt update

print('JUKEBOX - Upgrade any outdated packages...')
sudo apt upgrade

print('JUKEBOX - Remove any unused packages...')
sudo apt autoremove

# Install Apache Web Server
print('JUKEBOX - Install Apache2 Web Server...')
apt install apache2

# Replace Apache Config file
sudo cp /var/www/Jukebox/jukebox/server/jukebox.conf /etc/apache2/sites-available/jukebox.conf
sudo a2ensite jukebox

# Delete/replace application folder
print('JUKEBOX - Delete/create Jukebox application folder...')
sudo rm -R /var/www/Jukebox/
cd /var/www

# Download latest application code
print('JUKEBOX - Downloading code from GitHub...')
sudo git clone https://github.com/tjo234/Jukebox.git

# Create VirtualEnv
print('JUKEBOX - Setup Python Virtual Environment...')
cd /var/www/Jukebox
sudo python3 -m venv .env
source .env/bin/activate

# Install dependencies into VirtualEnv
print('JUKEBOX - Install dependencies...')
sudo pip install -r requirements.txt

# Create database 
print('JUKEBOX - Create Database folder and set permissions...')
sudo mkdir /var/database
sudo chown -R www-data:www-data /var/database
sudo chmod -R u+w /var/database

# Restart Apache Server
print('JUKEBOX - Restart Apache Server...')
sudo systemctl reload apache2

# Add latest updates for MPD on RaspberryPi OS Bullseye
# More info: https://kaliko.me/debian/
print('JUKEBOX - Download latest MPD packages from custom repo...')
sudo wget -O /tmp/kaliko-keyring.deb https://deb.kaliko.me/kaliko-archive-keyring.deb
sudo apt install /tmp/kaliko-keyring.deb
distribution=$(lsb_release -si|tr '[:upper:]' '[:lower:]')
release=$(lsb_release -sc)
echo "deb [signed-by=/usr/share/keyrings/deb.kaliko.me.gpg] \
  https://deb.kaliko.me/${distribution}-backports/ ${release}-backports main" \
  > /etc/apt/sources.list.d/deb.kaliko.me.list

# Update APT Package
print('JUKEBOX - Updating MPD package...')
sudo apt update

# Install Music Player Daemon
print('JUKEBOX - Installing MPD...')
apt install mpd

# Update MPD config file
sudo cp /var/www/Jukebox/jukebox/mpd/mpd.conf /etc/mpd/mpd.conf

# Update MPD config file
sudo systemctl reload apache2