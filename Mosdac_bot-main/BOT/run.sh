#!/bin/bash

echo "Starting ISRO ChatBot Application..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check if MongoDB is running
echo "Checking MongoDB connection..."
if ! python3 -c "from pymongo import MongoClient; client = MongoClient('mongodb://localhost:27017/'); client.admin.command('ping'); print('MongoDB is running')" 2>/dev/null; then
    echo "MongoDB is not running or not accessible"
    echo "Please start MongoDB service"
    echo "Linux/macOS: sudo systemctl start mongod"
    echo
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start the Flask application
echo
echo "Starting Flask application..."
echo "Application will be available at: http://localhost:5000"
echo
python app.py
