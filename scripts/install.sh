echo '''
-------------------------------------------------------------------------------

*** JUKEBOX INSTALLER ***

This will install the latest version of jukebox and its dependencies.

You should be able to run it multiple times without any issue. 

-------------------------------------------------------------------------------

'''

# Change to root
sudo -i

# Update APT to latest version
echo -e "\n\n***************** \n\nJUKEBOX - Update APT installer to latest version..."
apt update

echo -e "\n\n***************\n\nJUKEBOX - Upgrade any outdated packages...\n\n"
apt -y upgrade

echo -e "\n\n***************\n\nJUKEBOX - Remove any unused packages...\n\n"
apt -y autoremove

# Install Apache Web Server
echo -e "\n\n***************\n\nJUKEBOX - Install Apache2 WSGI...\n\n"
apt -y install apache2
apt -y install apache2-dev

# Remove default config
rm /etc/apache2/sites-enabled/000-default.conf

# Download latest application code
echo -e "\n\n***************\n\nJUKEBOX - Downloading code from GitHub...\n\n"
git clone https://github.com/tjo234/Jukebox.git /var/www/Jukebox

echo -e "\n\n***************\n\nJUKEBOX - Make VirtualEnvironment...\n\n"
cd /var/www/Jukebox
python3 -m venv .env
source .env/bin/activate

echo -e "\n\n***************\n\nJUKEBOX - Install dependencies...\n\n"
pip install -r requirements.txt

# Install mod_wsgi
echo -e "\n\n***************\n\nJUKEBOX - Install mod_wsgi...\n\n"
pip install mod_wsgi

# Replace Apache Config file
echo -e "\n\n***************\n\nJUKEBOX - Enable Jukebox config mod_wsgi...\n\n"
cp /var/www/Jukebox/setup/apache.conf /etc/apache2/sites-available/jukebox.conf
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

# Refresh packages
apt update

# Exit SuperUser Mode
exit

# Install Music Player Daemon as normal user
echo -e "\n\n***************\n\nJUKEBOX - Installing MPD...\n\n"
apt -y install mpd/bullseye-backports

# Run MPD server on-demand
echo -e "\n\n***************\n\nJUKEBOX - Running MPD Server...\n\n"
systemctl enable mpd.socket
systemctl start mpd.socket

# Back to SuperUser
sudo -i

MUSIC_DIR=/var/lib/mpd/music

# Add test file
cp /var/www/Jukebox/setup/test.mp3 $MUSIC_DIR

# Add Symlinks
ln -s /media/pi/MUSIC/ $MUSIC_DIR/MUSIC
ln -s /media/pi/JUKEBOX/ $MUSIC_DIR/JUKEBOX
ln -s /media/pi/MP3/ $MUSIC_DIR/MP3

# Exit SuperUser Mode
exit