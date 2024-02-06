echo -e """\n\n
-------------------------------------------------------------------------------

*** JUKEBOX INSTALLER ***

This will install the latest version of jukebox and its dependencies.

You should be able to run it multiple times without any issue. 

-------------------------------------------------------------------------------
\n\n"""

TS=$(date +%Y_%m_%d_%H_%M_%S)

# Change to root
sudo -i

# Delete/replace application folder
echo -e "\n\n***************\n\nJUKEBOX - Delete/create Jukebox application folder...\n\n"

mv /var/www/Jukebox /var/www/Jukebox_$TS

#rm -R /var/www/Jukebox

# Download latest application code
echo -e "\n\n***************\n\nJUKEBOX - Downloading code from GitHub...\n\n"
git clone --depth 1 https://github.com/tjo234/Jukebox.git /var/www/Jukebox

# Create VirtualEnv
echo -e "\n\n***************\n\nJUKEBOX - Setup Python Virtual Environment...\n\n"
cd /var/www/Jukebox
python3 -m venv .env
source .env/bin/activate

# Install dependencies into VirtualEnv
echo -e "\n\n***************\n\nJUKEBOX - Install dependencies...\n\n"
pip install -r requirements.txt

# Create cache folder for albums
mkdir /var/www/Jukebox/jukebox/static/img/albums
chmod 777 /var/www/Jukebox/jukebox/static/img/albums 
cp /var/www/Jukebox_$TS/jukebox/static/img/albums/ /var/www/Jukebox/jukebox/static/img/albums

# Exit SuperUser Mode
exit

