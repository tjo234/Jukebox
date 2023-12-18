echo '''\n\n
-------------------------------------------------------------------------------

*** JUKEBOX INSTALLER ***

This will install the latest version of jukebox and its dependencies.

You should be able to run it multiple times without any issue. 

-------------------------------------------------------------------------------
\n\n

'''

# Exit on error
set -e

# Change to root
sudo -i

# Update APT to latest version
echo -e "\\n*** JUKEBOX - Update APT installer to latest version..."
apt update

echo -e "\n\n***************\n\nJUKEBOX - Upgrade any outdated packages...\n\n"
apt -y upgrade

echo -e "\n\n***************\n\nJUKEBOX - Remove any unused packages...\n\n"
apt -y autoremove

# Install Apache Web Server
echo -e "\n\n***************\n\nJUKEBOX - Install Apache2 WSGI...\n\n"
apt -y install apache2
apt -y install libapache2-mod-wsgi-py3

# Delete/replace application folder
echo -e "\n\n***************\n\nJUKEBOX - Delete/create Jukebox application folder...\n\n"
rm -R /var/www/Jukebox

# Download latest application code
echo -e "\n\n***************\n\nJUKEBOX - Downloading code from GitHub...\n\n"
git clone https://github.com/tjo234/Jukebox.git /var/www/Jukebox

# Create VirtualEnv
echo -e "\n\n***************\n\nJUKEBOX - Setup Python Virtual Environment...\n\n"
cd /var/www/Jukebox
python3 -m venv .env
source .env/bin/activate

# Install dependencies into VirtualEnv
echo -e "\n\n***************\n\nJUKEBOX - Install dependencies...\n\n"
pip install -r requirements.txt

# Create database 
echo -e "\n\n***************\n\nJUKEBOX - Create Database folder and set permissions...\n\n"
mkdir /var/database
chown -R www-data:www-data /var/database
chmod -R u+w /var/database

# Replace Apache Config file
cp /var/www/Jukebox/jukebox/config/jukebox.conf /etc/apache2/sites-available/jukebox.conf
a2ensite jukebox

# Restart Apache Server
echo -e "\n\n***************\n\nJUKEBOX - Restart Apache Server...\n\n"
systemctl reload apache2

# Add latest updates for MPD on RaspberryPi OS Bullseye
# More info: https://kaliko.me/debian/
echo -e "\n\n***************\n\nJUKEBOX - Download latest MPD packages from custom repo...\n\n"
wget -O /tmp/kaliko-keyring.deb https://deb.kaliko.me/kaliko-archive-keyring.deb
apt install /tmp/kaliko-keyring.deb
distribution=$(lsb_release -si|tr "[:upper:]" "[:lower:]")
release=$(lsb_release -sc)
echo -e "deb [signed-by=/usr/share/keyrings/deb.kaliko.me.gpg] \
  https://deb.kaliko.me/${distribution}-backports/ ${release}-backports main" \
  > /etc/apt/sources.list.d/deb.kaliko.me.list

# Exit SuperUser Mode
exit

# Install Music Player Daemon as normal user
echo -e "\n\n***************\n\nJUKEBOX - Installing MPD...\n\n"
sudo apt -y install mpd

# Back to SuperUse
sudo -i

# Update MPD config file
echo -e "\n\n***************\n\nJUKEBOX - Update config file...\n\n"
sudo cp /var/www/Jukebox/jukebox/config/mpd.conf ~/.config/mpd/mpd.conf

# Copy test file into library
cp /var/www/Jukebox/jukebox/audio/test.flac /var/lib/mpd/music

# Update MPD config file
echo -e "\n\n***************\n\nJUKEBOX - Reload Music Player Daemon...\n\n"
sudo systemctl restart mpd

# Exit SuperUser Mode
exit