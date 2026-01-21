#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Setting up virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

if [ ! -d "migrations" ]; then
    echo "Initializing migrations folder..."
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
else
    echo "Migrations exist. Upgrading database..."
    flask db upgrade
fi

echo "Installation complete. Run 'source .venv/bin/activate' to start."
