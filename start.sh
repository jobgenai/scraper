#!/bin/bash

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install Chrome and Chromedriver
echo "Installing Chrome and Chromedriver..."
apt-get update
apt-get install -y wget unzip google-chrome-stable chromium-chromedriver

# Set environment variables
export GOOGLE_CHROME_BIN=/usr/bin/google-chrome
export CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Start the Flask server
echo "Starting the web server..."
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=5000
