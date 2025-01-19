#!/bin/bash

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install Google Chrome
echo "Installing Chrome..."
apt-get update
apt-get install -y wget unzip
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable_current_amd64.deb || apt-get -f install -y

# Export the Chrome binary path
export GOOGLE_CHROME_BIN=/usr/bin/google-chrome

# Debugging: Check Chrome installation
echo "Installed Chrome version:"
google-chrome --version

# Start the Flask server
echo "Starting the web server..."
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=5000
