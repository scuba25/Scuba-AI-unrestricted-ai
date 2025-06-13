# 🤿 Scuba AI Chat

**An advanced, unfiltered AI chat assistant with a sleek web interface**

Scuba AI is a powerful Flask-based web application that provides an unrestricted AI chat experience using the Groq API. Features a modern, mobile-responsive interface with PWA capabilities and persistent conversation history.

![Scuba AI Interface](https://img.shields.io/badge/Interface-Mobile%20Responsive-blue)
![Python](https://img.shields.io/badge/Python-3.7+-green)
![Flask](https://img.shields.io/badge/Flask-2.0+-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- **🤖 Advanced AI Integration**: Powered by Groq's fast LLM API
- **📱 Mobile-First Design**: Responsive interface optimized for all devices
- **💾 Persistent Conversations**: Sessions saved with automatic cleanup
- **🔧 PWA Ready**: Can be installed as a mobile/desktop app
- **🎨 Modern UI**: Gradient design with dark purple accents
- **⚡ Real-time Chat**: Instant responses with typing indicators
- **🔒 Session Management**: Secure conversation handling
- **🌙 Clean Architecture**: Well-structured Flask application

## 🚀 Quick Start

### Option 1: Automated Installation (Recommended)

Run our one-command installer that sets up everything automatically:

```bash
curl -fsSL https://raw.githubusercontent.com/scuba25/Scuba-AI-unrestricted-ai/main/install.sh | bash
```

**Or download and run manually:**

```bash
wget https://raw.githubusercontent.com/scuba25/Scuba-AI-unrestricted-ai/main/install.sh
chmod +x install.sh
./install.sh
```

### Option 2: Manual Installation

#### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Git

#### Steps

1. **Clone the repository:**
```bash
git clone https://github.com/scuba25/Scuba-AI-unrestricted-ai.git
cd Scuba-AI-unrestricted-ai
```

2. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure API key:**
```bash
# Edit app.py and replace the GROQ_API_KEY with your own
# Or set as environment variable:
export GROQ_API_KEY="your_groq_api_key_here"
```

5. **Run the application:**
```bash
python app.py
```

6. **Access the app:**
Open your browser and go to `http://localhost:3000`

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root (optional):

```env
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=your_secret_key_here
PORT=3000
DEBUG=False
```

### API Key Setup

1. Get your Groq API key from [Groq Console](https://console.groq.com)
2. Either:
   - Set the `GROQ_API_KEY` environment variable, or
   - Replace the key directly in `app.py` (line 11)

## 📁 Project Structure

```
scuba-ai/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── install.sh            # Automated installation script
├── README.md             # This file
├── conversations.json    # Conversation storage (auto-generated)
├── static/               # Static files (if needed)
└── templates/            # HTML templates (embedded in app.py)
```

## 🖥️ System Requirements

- **Operating System**: Linux, macOS, Windows
- **Python**: 3.7 or higher
- **Memory**: 512MB RAM minimum
- **Storage**: 100MB free space
- **Network**: Internet connection for API calls

## 🔒 Security Features

- Session-based conversation management
- Automatic cleanup of old conversations (24h)
- CSRF protection with secret keys
- Input validation and sanitization
- Error handling for API failures

## 📱 PWA Installation

The app can be installed as a Progressive Web App:

1. Open the app in your mobile browser
2. Look for the "Install App" prompt
3. Follow browser-specific installation steps
4. Launch from your home screen like a native app

## 🛠️ Development

### Running in Development Mode

```bash
export FLASK_ENV=development
export DEBUG=True
python app.py
```

### API Endpoints

- `GET /` - Main chat interface
- `POST /api/chat` - Send message to AI
- `POST /api/clear` - Clear conversation history
- `GET /health` - Health check endpoint
- `GET /manifest.json` - PWA manifest

## 🚀 Deployment

### Production Deployment

1. **Set production environment:**
```bash
export FLASK_ENV=production
export DEBUG=False
```

2. **Use a production WSGI server:**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:3000 app:app
```

### Docker Deployment

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 3000
CMD ["python", "app.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📋 Changelog

### v1.0.0
- Initial release with full chat functionality
- Mobile-responsive design
- PWA capabilities
- Session management
- Automated installation script

## ⚠️ Important Notes

- **API Usage**: This app uses the Groq API which may have usage limits
- **Data Storage**: Conversations are stored locally in `conversations.json`
- **Security**: The system prompt contains specific AI behavior instructions
- **Compliance**: Ensure your usage complies with Groq's terms of service

## 🆘 Troubleshooting

### Common Issues

1. **API Key Error**: Make sure your Groq API key is valid and properly set
2. **Port Already in Use**: Change the port in `app.py` or kill the process using port 3000
3. **Permission Denied**: Ensure you have write permissions in the project directory
4. **Module Not Found**: Make sure you've activated your virtual environment and installed dependencies

### Getting Help

- Check the [Issues](https://github.com/scuba25/Scuba-AI-unrestricted-ai/issues) page
- Create a new issue with detailed error information
- Include your Python version, OS, and error logs

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⭐ Support

If you found this project helpful, please give it a star! ⭐

---

**Disclaimer**: This AI assistant is designed to be unfiltered and provide comprehensive responses. Use responsibly and in accordance with applicable laws and regulations.