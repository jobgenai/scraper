#!/bin/bash

# Ensure dependencies are installed
echo "Installing dependencies..."
pip install -r requirements.txt

# Start the Flask server
echo "Starting the web server..."
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=5000
