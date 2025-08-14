# ISRO ChatBot Project

A comprehensive chatbot application built with Flask, MongoDB, and Streamlit for ISRO (Indian Space Research Organisation) related queries and space exploration assistance.

## Features

### 🔐 Authentication System

- User registration and login
- Secure password hashing
- Session management
- Beautiful responsive UI

### 💬 Chatbot Interface

- Real-time chat interface
- ISRO-focused responses
- Chat history storage
- Typing indicators
- Message formatting

### 📊 Analytics Dashboard (Streamlit)

- User behavior analytics
- Chat statistics
- Performance metrics
- ISRO mission data visualization

### 🗄️ Database Integration

- MongoDB for data storage
- User management
- Chat history tracking
- Session persistence

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: MongoDB
- **Frontend**: HTML5, CSS3, JavaScript
- **Analytics**: Streamlit
- **Authentication**: Werkzeug Security
- **Styling**: Custom CSS with animations

## Project Structure

```
BOT/
├── app.py                 # Main Flask application
├── streamlit_app.py       # Streamlit analytics dashboard
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/            # HTML templates
│   ├── login.html        # Login/Register page
│   └── chatbot.html      # Chat interface
└── static/              # Static assets
    ├── css/
    │   └── style.css     # Main stylesheet
    └── js/
        ├── auth.js       # Authentication JavaScript
        └── chatbot.js    # Chat functionality
```

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- MongoDB installed and running
- Git (optional)

### 1. Clone or Download the Project

```bash
git clone <repository-url>
cd BOT
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup MongoDB

Make sure MongoDB is installed and running on your system:

- Windows: Download from MongoDB official website
- Linux: `sudo apt-get install mongodb`
- macOS: `brew install mongodb`

Start MongoDB service:

```bash
# Windows
net start MongoDB

# Linux/macOS
sudo systemctl start mongod
```

### 4. Run the Flask Application

```bash
python app.py
```

The application will be available at: `http://localhost:5000`

### 5. Run the Streamlit Dashboard (Optional)

In a new terminal:

```bash
streamlit run streamlit_app.py
```

The dashboard will be available at: `http://localhost:8501`

## Usage

### 1. Authentication

1. Navigate to `http://localhost:5000`
2. Create a new account or login with existing credentials
3. You'll be redirected to the chatbot interface

### 2. Chatbot Features

- Ask questions about ISRO missions, satellites, space technology
- Use suggested questions for quick start
- View chat history in the sidebar
- Clear conversations when needed

### 3. Analytics Dashboard

- Monitor user engagement
- View conversation statistics
- Analyze user behavior patterns
- Explore ISRO mission data

## Configuration

### Database Configuration

The application connects to MongoDB at `mongodb://localhost:27017/` by default. You can modify the connection string in `app.py`:

```python
client = MongoClient('mongodb://localhost:27017/')
db = client['chatbot_app']
```

### Environment Variables (Optional)

You can create a `.env` file for configuration:

```
MONGODB_URI=mongodb://localhost:27017/
SECRET_KEY=your_secret_key_here
FLASK_ENV=development
```

## API Endpoints

- `GET /` - Redirect to login or chatbot
- `GET /login` - Login page
- `POST /login` - Authenticate user
- `POST /register` - Register new user
- `GET /chatbot` - Chat interface (requires authentication)
- `POST /chat` - Send message to chatbot
- `GET /chat_history` - Retrieve user's chat history
- `GET /logout` - Logout user

## Customization

### Adding New Chatbot Responses

Modify the `generate_bot_response()` function in `app.py`:

```python
def generate_bot_response(message):
    # Add your custom logic here
    # You can integrate with AI/ML models, APIs, etc.
    pass
```

### Styling Customization

Edit `static/css/style.css` to customize the appearance:

- Colors and themes
- Animations
- Layout adjustments
- Responsive design

### Adding New Features

1. **Backend**: Add new routes in `app.py`
2. **Frontend**: Update HTML templates and JavaScript
3. **Database**: Modify MongoDB collections as needed

## Troubleshooting

### Common Issues

1. **MongoDB Connection Error**

   - Ensure MongoDB is running
   - Check connection string in `app.py`
   - Verify firewall settings

2. **Port Already in Use**

   - Change port in `app.py`: `app.run(debug=True, port=5001)`
   - Kill existing processes: `netstat -ano | findstr :5000`

3. **Module Import Errors**

   - Reinstall dependencies: `pip install -r requirements.txt`
   - Check Python version compatibility

4. **Static Files Not Loading**
   - Clear browser cache
   - Check file paths in templates
   - Ensure Flask static folder configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For support and questions:

- Create an issue in the repository
- Email: your-email@example.com

## Future Enhancements

- [ ] AI/ML integration for smarter responses
- [ ] Voice chat capabilities
- [ ] Multi-language support
- [ ] Advanced analytics
- [ ] Mobile app development
- [ ] Integration with ISRO APIs
- [ ] Real-time notifications
- [ ] Export chat history

## Acknowledgments

- ISRO for inspiration and space exploration data
- Flask and Streamlit communities
- MongoDB for database solutions
- Contributors and testers

---

**Made with ❤️ for space exploration enthusiasts**
