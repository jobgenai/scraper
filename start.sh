#!/bin/bash

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install Chrome and Chromedriver with root privileges
echo "Installing Chrome and Chromedriver..."
apt-get update -y
apt-get install -y wget unzip
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable_current_amd64.deb || apt-get -f install -y
apt-get install -y chromium-chromedriver

# Set environment variables for Chrome and Chromedriver
export GOOGLE_CHROME_BIN=/usr/bin/google-chrome
export CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Debugging: Verify installations
echo "Installed Chrome version:"
google-chrome --version || echo "Chrome installation failed"
echo "Installed Chromedriver version:"
chromedriver --version || echo "Chromedriver installation failed"

# Start the Flask server
echo "Starting the web server..."
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=5000
