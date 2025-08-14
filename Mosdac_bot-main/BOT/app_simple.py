from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import secrets
import json
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Simple file-based storage (for testing without MongoDB)
USERS_FILE = 'users.json'
CHATS_FILE = 'chats.json'

def load_json_file(filename):
    """Load data from JSON file"""
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_json_file(filename, data):
    """Save data to JSON file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, default=str)

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
        
        users = load_json_file(USERS_FILE)
        user = users.get(username)
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = username
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
    
    users = load_json_file(USERS_FILE)
    
    # Check if user already exists
    if username in users:
        return jsonify({'success': False, 'message': 'Username already exists!'})
    
    # Check if email already exists
    for user_data in users.values():
        if user_data.get('email') == email:
            return jsonify({'success': False, 'message': 'Email already registered!'})
    
    # Create new user
    hashed_password = generate_password_hash(password)
    users[username] = {
        'username': username,
        'email': email,
        'password': hashed_password,
        'created_at': datetime.now().isoformat()
    }
    
    save_json_file(USERS_FILE, users)
    
    session['user_id'] = username
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
    
    # Simple chatbot response
    bot_response = generate_bot_response(message)
    
    # Save chat to file
    chats = load_json_file(CHATS_FILE)
    user_id = session['user_id']
    
    if user_id not in chats:
        chats[user_id] = []
    
    chat_entry = {
        'user_message': message,
        'bot_response': bot_response,
        'timestamp': datetime.now().isoformat()
    }
    
    chats[user_id].append(chat_entry)
    save_json_file(CHATS_FILE, chats)
    
    return jsonify({'response': bot_response})

@app.route('/chat_history')
def chat_history():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    chats = load_json_file(CHATS_FILE)
    user_chats = chats.get(session['user_id'], [])
    
    return jsonify({'chats': user_chats})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

def generate_bot_response(message):
    """Enhanced chatbot logic with more ISRO-specific responses"""
    message_lower = message.lower()
    
    # ISRO Missions
    if 'chandrayaan' in message_lower:
        if '3' in message:
            return """🌙 **Chandrayaan-3 Mission**

India's most successful lunar mission! Here are the key highlights:

**Launch**: July 14, 2023
**Landing**: August 23, 2023 (South Pole)

🎯 **Achievements**:
- Successful soft landing near lunar south pole
- Made India the 4th country to land on Moon
- First to land near lunar south pole
- Vikram lander and Pragyan rover operated successfully
- Discovered sulfur and other elements on lunar surface

**Cost**: ₹615 crores (extremely cost-effective!)

The mission proved India's growing space capabilities and ISRO's frugal engineering approach."""
        
        elif '2' in message:
            return """🌙 **Chandrayaan-2 Mission**

**Launch**: July 22, 2019
**Status**: Partial success

🛰️ **Components**:
- Orbiter: Still operational and sending valuable data
- Vikram Lander: Hard landing, couldn't establish communication
- Pragyan Rover: Couldn't deploy due to lander issues

**Key Discoveries**:
- Water molecules confirmed on Moon
- Detailed lunar surface mapping
- Mineral composition analysis

Despite the landing challenges, the orbiter continues to provide crucial scientific data!"""
        
        else:
            return """🌙 **Chandrayaan Series - India's Lunar Exploration**

**Chandrayaan-1** (2008): India's first Moon mission
- Discovered water molecules on Moon
- 312 days of operation
- Made India the 5th country to reach Moon

**Chandrayaan-2** (2019): Orbiter + Lander + Rover
- Orbiter still operational
- Advanced lunar studies

**Chandrayaan-3** (2023): Historic success!
- First to land near lunar south pole
- Made India the 4th country to achieve soft landing

What specific aspect would you like to know more about?"""
    
    elif 'mangalyaan' in message_lower or 'mars' in message_lower:
        return """🔴 **Mars Orbiter Mission (Mangalyaan)**

**Launch**: November 5, 2013
**Journey**: 298 days to Mars
**Cost**: $74 million (cheaper than Hollywood movie Gravity!)

🏆 **Historic Achievements**:
- First Asian country to reach Mars orbit
- First country to succeed in first attempt
- Most cost-effective Mars mission ever
- Operated for 8 years (planned for 6 months)

🔬 **Scientific Discoveries**:
- Methane detection in Martian atmosphere
- Dust storm monitoring
- Surface feature mapping
- Atmospheric studies

**Fun Fact**: The entire mission cost less than a New York to London flight for every Indian citizen!"""
    
    elif 'aditya' in message_lower or 'sun' in message_lower:
        return """☀️ **Aditya-L1 Mission**

India's first solar mission!

**Launch**: September 2, 2023
**Destination**: L1 Lagrange point (1.5 million km from Earth)
**Mission Duration**: 5 years

🔬 **Objectives**:
- Study solar corona and solar wind
- Understand space weather
- Monitor solar flares and their impact on Earth
- Coronal mass ejection studies

**Significance**: 
- Will help predict space weather
- Crucial for satellite and communication protection
- Advance our understanding of solar physics

This mission positions India among elite space-faring nations studying our Sun!"""
    
    elif 'pslv' in message_lower or 'launch vehicle' in message_lower:
        return """🚀 **PSLV (Polar Satellite Launch Vehicle)**

ISRO's most reliable workhorse!

**Key Features**:
- 4-stage rocket (solid-liquid-solid-liquid)
- Height: 44 meters
- Payload capacity: 3,800 kg to LEO

🏆 **Achievements**:
- 50+ successful launches
- 99% success rate
- Launched 400+ satellites
- Record: 104 satellites in single mission (2017)

**Famous Missions**:
- Chandrayaan-1 & 2
- Mars Orbiter Mission
- Multiple foreign satellites

**Why it's special**: Extremely reliable and cost-effective!"""
    
    elif 'gslv' in message_lower:
        return """🚀 **GSLV (Geosynchronous Satellite Launch Vehicle)**

ISRO's heavy-lift champion!

**Variants**:
- GSLV Mk II: 2,500 kg to GTO
- GSLV Mk III: 4,000 kg to GTO (now called LVM3)

**Key Features**:
- Indigenous cryogenic engine
- Can launch communication satellites
- Enables India's self-reliance in heavy launches

**Recent Success**: GSLV Mk III launched Chandrayaan-3!

This vehicle reduces India's dependence on foreign launchers for heavy satellites."""
    
    elif 'satellite' in message_lower:
        return """🛰️ **ISRO's Satellite Programs**

**Major Satellite Series**:

📡 **INSAT**: Communication & Broadcasting
📡 **IRS**: Earth Observation & Remote Sensing  
📡 **RISAT**: Radar Imaging (all-weather)
📡 **NavIC/IRNSS**: India's GPS system
📡 **Astrosat**: Space astronomy

**Recent Launches**:
- EOS series for Earth observation
- EMISAT for electromagnetic intelligence
- Cartosat for high-resolution imaging

**Fun Fact**: ISRO has launched 400+ satellites, including many for foreign countries, earning valuable foreign exchange!

Which satellite program interests you most?"""
    
    elif 'gaganyaan' in message_lower or 'human' in message_lower:
        return """👨‍🚀 **Gaganyaan Mission**

India's first human spaceflight program!

**Timeline**: First crewed mission planned for 2025
**Crew**: 3 Indian astronauts (Vyomanauts)
**Duration**: 3 days in Low Earth Orbit

🎯 **Mission Profile**:
- Crew module can carry 3 astronauts
- Automated docking capability
- Advanced life support systems
- Emergency escape system

**Current Status**:
- Astronaut training in Russia completed
- Test flights being conducted
- Ground testing in progress

This will make India the 4th country to independently send humans to space!"""
    
    elif 'future' in message_lower or 'upcoming' in message_lower:
        return """🔮 **ISRO's Future Missions**

**Upcoming Missions**:

🌙 **Chandrayaan-4**: Sample return mission
🔴 **Mars Lander Mission**: Following Mangalyaan's success
🪐 **Shukrayaan-1**: Venus orbiter mission
👨‍🚀 **Gaganyaan**: Human spaceflight
🛰️ **Space Station**: Indian space station by 2030

**Ambitious Goals**:
- Reusable launch vehicles (RLV-TD testing)
- Interplanetary missions to Jupiter/Saturn
- Lunar base establishment
- Commercial space ventures

**Vision 2030**: ISRO aims to be a major global space power with indigenous capabilities across all domains!"""
    
    elif any(word in message_lower for word in ['hello', 'hi', 'hey']):
        return """🚀 **Hello, Space Explorer!**

Welcome to ISRO ChatBot! I'm here to help you discover the amazing world of Indian space exploration.

**What I can help you with**:
- 🌙 Lunar missions (Chandrayaan series)
- 🔴 Mars exploration (Mangalyaan)
- ☀️ Solar studies (Aditya-L1)
- 🚀 Launch vehicles (PSLV, GSLV)
- 🛰️ Satellite programs
- 👨‍🚀 Human spaceflight (Gaganyaan)
- 🔮 Future missions

Ask me anything about ISRO's incredible journey among the stars! What fascinates you most about space exploration?"""
    
    elif any(word in message_lower for word in ['help', 'what can you do']):
        return """🤖 **ISRO ChatBot Help**

I'm your personal guide to India's space program! Here's what you can explore:

**🔥 Popular Topics**:
- "Tell me about Chandrayaan-3"
- "What is Mangalyaan?"
- "ISRO future missions"
- "PSLV vs GSLV difference"
- "How does NavIC work?"

**🎯 Mission Categories**:
- Lunar missions
- Planetary exploration  
- Earth observation
- Communication satellites
- Scientific missions

**💡 Pro Tips**:
- Ask specific questions for detailed answers
- Mention mission names for targeted information
- I can explain complex concepts simply!

What would you like to explore first?"""
    
    elif 'thank' in message_lower:
        return """🙏 **You're Welcome!**

I'm glad I could help you learn about ISRO's amazing achievements! 

Space exploration is truly inspiring, and India's journey has been remarkable - from our first satellite Aryabhatta in 1975 to landing on the Moon's south pole in 2023!

Feel free to ask me anything else about:
- Mission details
- Technical specifications  
- Historical achievements
- Future plans

Keep exploring the cosmos! 🌟🚀"""
    
    elif any(word in message_lower for word in ['bye', 'goodbye']):
        return """👋 **Safe Travels, Space Explorer!**

Thank you for exploring India's space journey with me! 

Remember: "The sky is not the limit; it's just the beginning!" 🚀

Come back anytime to discover more about ISRO's incredible missions and India's growing presence in space.

Until next time, keep looking up at the stars! ⭐🌙"""
    
    else:
        return f"""🤔 **Interesting question about: "{message}"**

I'd love to help you explore that topic! Here are some ways I can assist:

**🚀 ISRO Missions**: Chandrayaan, Mangalyaan, Aditya-L1
**🛰️ Satellites**: Communication, Earth observation, Navigation
**🚀 Launch Vehicles**: PSLV, GSLV capabilities
**👨‍🚀 Human Spaceflight**: Gaganyaan program
**🔮 Future Plans**: Upcoming missions and goals

Could you be more specific about what aspect of space exploration interests you? I have detailed information about all of ISRO's achievements and programs!"""

if __name__ == '__main__':
    print("🚀 Starting ISRO ChatBot (Simplified Version)")
    print("📱 Application will be available at: http://localhost:5000")
    print("✨ Features: Login, Register, Chat, History")
    print("💾 Using file-based storage (no MongoDB required)")
    print("-" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
