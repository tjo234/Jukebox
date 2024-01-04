# Create Virtual Environment
python3 -m venv .env

# Activate Virtual Environments
source .env/bin/activate

# Install dependencies into VirtualEnv
pip install -r requirements.txt

# Start Flask Development server
python3 main.py