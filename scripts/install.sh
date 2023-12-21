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
echo -e "\\n*** JUKEBOX - Update APT installer to latest version..."
apt update

echo -e "\n\n***************\n\nJUKEBOX - Upgrade any outdated packages...\n\n"
apt -y upgrade

echo -e "\n\n***************\n\nJUKEBOX - Remove any unused packages...\n\n"
apt -y autoremove

# Install Apache Web Server
echo -e "\n\n***************\n\nJUKEBOX - Install Apache2 WSGI...\n\n"
apt -y install apache2
apt -y install apache2-dev

# Delete/replace application folder
echo -e "\n\n***************\n\nJUKEBOX - Delete/create Jukebox application folder...\n\n"
rm -R /var/www/Jukebox

# Download latest application code
echo -e "\n\n***************\n\nJUKEBOX - Downloading code from GitHub...\n\n"
git clone https://github.com/tjo234/Jukebox.git /var/www/Jukebox

# Create VirtualEnv
echo -e "\n\n***************\n\nJUKEBOX - Setup Python Virtual Environment...\n\n"
cd /var/www/Jukebox

# Install dependencies into VirtualEnv
echo -e "\n\n***************\n\nJUKEBOX - Install dependencies...\n\n"
pip install -r requirements.txt

# Install mod_wsgi into VirtualEnv
pip install mod_wsgi

# Replace Apache Config file
cp /var/www/Jukebox/setup/apache.conf /etc/apache2/sites-available/jukebox.conf
a2ensite jukebox

# Remove default config
rm /etc/apache2/sites-available/000-default.conf

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
sudo apt -y install mpd/bullseye-backports

# Run MPD server
mpd

# Back to SuperUser
sudo -i

# Update MPD config file
echo -e "\n\n***************\n\nJUKEBOX - Update config file...\n\n"
sudo cp /var/www/Jukebox/setup/mpd.conf /etc/mpd.conf

# Update MPD config file
echo -e "\n\n***************\n\nJUKEBOX - Reload Music Player Daemon...\n\n"
sudo systemctl restart mpd

# Create database 
echo -e "\n\n***************\n\nJUKEBOX - Create Database folder and set permissions...\n\n"
# mkdir /var/database
# chown -R www-data:www-data /var/database
# chmod -R u+w /var/database

# # Add Jukebox folder
# mkdir /jukebox
# chmod 777 /jukebox
# cp /var/www/Jukebox/setup/intro.mov /jukebox/
# cp /var/www/Jukebox/setup/desktop.png /jukebox/

# # Add Music Folder
# mkdir /jukebox/music
# chmod 777 /jukebox/music

MUSIC_DIR=/var/lib/mpd/music

# Add test file
cp /var/www/Jukebox/setup/test.mp3 $MUSIC_DIR

# Add desktop symlink
ln -s $MUSIC_DIR /home/pi/Desktop/Music

# Add External Symlinks
ln -s /media/pi/MEDIA/ $MUSIC_DIR/media
ln -s /media/pi/MUSIC/ $MUSIC_DIR/music
ln -s /media/pi/JUKEBOX/ $MUSIC_DIR/jukebox

# Add Video Playlist on Startup
mkdir /home/pi/.config/autostart
cp /var/www/Jukebox/setup/autovlc.desktop /home/pi/.config/autostart/
cp /var/www/Jukebox/setup/playlist.m3u /home/pi/

# Exit SuperUser Mode
exit