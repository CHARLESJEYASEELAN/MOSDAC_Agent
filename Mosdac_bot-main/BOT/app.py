from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from datetime import datetime
import os
from bson import ObjectId
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# MongoDB configuration
try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['chatbot_app']
    users_collection = db['users']
    chats_collection = db['chats']
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"MongoDB connection error: {e}")

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('chatbot'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = users_collection.find_one({'username': username})
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
            return jsonify({'success': True, 'message': 'Login successful!'})
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials!'})
    
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    

    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    # Check if user already exists
    if users_collection.find_one({'username': username}):
        return jsonify({'success': False, 'message': 'Username already exists!'})
    
    if users_collection.find_one({'email': email}):
        return jsonify({'success': False, 'message': 'Email already registered!'})
    
    # Create new user
    hashed_password = generate_password_hash(password)
    user_data = {
        'username': username,
        'email': email,
        'password': hashed_password,
        'created_at': datetime.now()
    }
    
    result = users_collection.insert_one(user_data)
    session['user_id'] = str(result.inserted_id)
    print("All users in DB:")
    for u in users_collection.find():
        print(u)
    session['username'] = username
    
    return jsonify({'success': True, 'message': 'Registration successful!'})

@app.route('/chatbot')
def chatbot():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('chatbot.html', username=session['username'])

@app.route('/chat', methods=['POST'])
def chat():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    message = data.get('message')
    
    # Simple chatbot response (you can integrate with AI services here)
    bot_response = generate_bot_response(message)
    
    # Save chat to database
    chat_data = {
        'user_id': ObjectId(session['user_id']),
        'user_message': message,
        'bot_response': bot_response,
        'timestamp': datetime.now()
    }
    chats_collection.insert_one(chat_data)
    
    return jsonify({'response': bot_response})

@app.route('/chat_history')
def chat_history():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    chats = list(chats_collection.find(
        {'user_id': ObjectId(session['user_id'])},
        {'_id': 0, 'user_message': 1, 'bot_response': 1, 'timestamp': 1}
    ).sort('timestamp', 1))
    
    # Convert datetime to string for JSON serialization
    for chat in chats:
        chat['timestamp'] = chat['timestamp'].isoformat()
    
    return jsonify({'chats': chats})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

def generate_bot_response(message):
    """Simple chatbot logic - replace with AI/ML model integration"""
    message_lower = message.lower()
    
    responses = {
        'hello': 'Hello! How can I help you today?',
        'hi': 'Hi there! What would you like to know?',
        'how are you': 'I\'m doing great, thank you for asking!',
        'bye': 'Goodbye! Have a great day!',
        'help': 'I\'m here to help! You can ask me questions about various topics.',
        'isro': 'ISRO (Indian Space Research Organisation) is India\'s national space agency. What would you like to know about ISRO?',
        'space': 'Space exploration is fascinating! Are you interested in satellites, missions, or space technology?',
        'mission': 'ISRO has conducted many successful missions including Chandrayaan, Mangalyaan, and more!',
    }
    
    for keyword, response in responses.items():
        if keyword in message_lower:
            return response
    
    return "That's interesting! Can you tell me more about what you'd like to know?"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
