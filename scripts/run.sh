# Create Virtual Environment
python3 -m venv .env

# Activate Virtual Environment
source .env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Export environment variables
export FLASK_DATABASE="sql/library.db"

# Run web server
python3 main.py