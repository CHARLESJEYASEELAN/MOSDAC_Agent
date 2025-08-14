# Quick Start Guide - ISRO ChatBot

## Option 1: Quick Run (Without MongoDB - Testing Only)

If you want to test the application quickly without setting up MongoDB, I'll create a simplified version:

### Step 1: Install Python packages

```bash
pip install flask werkzeug
```

### Step 2: Run the simplified app

```bash
python app_simple.py
```

## Option 2: Full Setup (With MongoDB)

### Step 1: Install MongoDB

1. Download MongoDB Community Server from: https://www.mongodb.com/try/download/community
2. Install with default settings
3. MongoDB will start automatically as a Windows service

### Step 2: Start MongoDB (if not running)

```bash
net start MongoDB
```

### Step 3: Install Python dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the full application

```bash
python app.py
```

## Step 3: Open in Browser

Navigate to: http://localhost:5000

## Features Available:

- ✅ Beautiful login/register page
- ✅ Secure authentication
- ✅ Interactive chatbot interface
- ✅ Chat history (with MongoDB)
- ✅ Responsive design
- ✅ Space-themed animations

## Optional: Streamlit Dashboard

```bash
streamlit run streamlit_app.py
```

Dashboard will be available at: http://localhost:8501
