echo '''\n\n
-------------------------------------------------------------------------------

*** JUKEBOX INSTALLER ***

This will install the latest version of jukebox and its dependencies.

You should be able to run it multiple times without any issue. 

-------------------------------------------------------------------------------
\n\n

'''

# Change to root
sudo -i

# Update APT to latest version
echo "JUKEBOX - Update APT installer to latest version..."
apt update

echo "JUKEBOX - Upgrade any outdated packages..."
apt -y upgrade

echo "JUKEBOX - Remove any unused packages..."
apt -y autoremove

# Install Apache Web Server
echo "JUKEBOX - Install Apache2 Web Server..."
apt -y install apache2

# Delete/replace application folder
echo "JUKEBOX - Delete/create Jukebox application folder..."
rm -R /var/www/Jukebox

# Download latest application code
echo "JUKEBOX - Downloading code from GitHub..."
git clone https://github.com/tjo234/Jukebox.git /var/www/Jukebox

# Create VirtualEnv
echo "JUKEBOX - Setup Python Virtual Environment..."
cd /var/www/Jukebox
python3 -m venv .env
source .env/bin/activate

# Install dependencies into VirtualEnv
echo "JUKEBOX - Install dependencies..."
pip install -r requirements.txt

# Create database 
echo "JUKEBOX - Create Database folder and set permissions..."
mkdir /var/database
chown -R www-data:www-data /var/database
chmod -R u+w /var/database

# Replace Apache Config file
cp /var/www/Jukebox/jukebox/config/jukebox.conf /etc/apache2/sites-available/jukebox.conf
a2ensite jukebox

# Restart Apache Server
echo "JUKEBOX - Restart Apache Server..."
systemctl reload apache2fF

# Add latest updates for MPD on RaspberryPi OS Bullseye
# More info: https://kaliko.me/debian/
echo "JUKEBOX - Download latest MPD packages from custom repo..."
wget -O /tmp/kaliko-keyring.deb https://deb.kaliko.me/kaliko-archive-keyring.deb
apt install /tmp/kaliko-keyring.deb
distribution=$(lsb_release -si|tr "[:upper:]" "[:lower:]")
release=$(lsb_release -sc)
echo "deb [signed-by=/usr/share/keyrings/deb.kaliko.me.gpg] \
  https://deb.kaliko.me/${distribution}-backports/ ${release}-backports main" \
  > /etc/apt/sources.list.d/deb.kaliko.me.list

# Exit SuperUser Mode
exit

# Install Music Player Daemon as normal user
echo "JUKEBOX - Installing MPD..."
sudo apt -y install mpd

# Back to SuperUse
sudo -i

# Update MPD config file
echo "JUKEBOX - Update config file..."
sudo cp /var/www/Jukebox/jukebox/config/mpd.conf ~/.config/mpd/mpd.conf

# Copy test file into library
cp /var/www/Jukebox/jukebox/audio/test.flac ~/jukebox

# Update MPD config file
echo "JUKEBOX - Reload Music Player Daemon..."
sudo systemctl reload apache2

# Exit SuperUser Mode
exit