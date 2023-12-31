echo -e """\n\n
-------------------------------------------------------------------------------

*** JUKEBOX INSTALLER ***

This will install the latest version of jukebox and its dependencies.

You should be able to run it multiple times without any issue. 

-------------------------------------------------------------------------------
\n\n"""

# Change to root
sudo -i

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

# Exit SuperUser Mode
exit