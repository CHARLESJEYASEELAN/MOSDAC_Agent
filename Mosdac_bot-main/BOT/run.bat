@echo off
echo Starting ISRO ChatBot Application...
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

:: Check if MongoDB is running
echo Checking MongoDB connection...
python -c "from pymongo import MongoClient; client = MongoClient('mongodb://localhost:27017/'); client.admin.command('ping'); print('MongoDB is running')" 2>nul
if errorlevel 1 (
    echo MongoDB is not running or not accessible
    echo Please start MongoDB service
    echo Windows: net start MongoDB
    echo.
    pause
    exit /b 1
)

:: Install requirements if needed
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

:: Start the Flask application
echo.
echo Starting Flask application...
echo Application will be available at: http://localhost:5000
echo.
python app.py
