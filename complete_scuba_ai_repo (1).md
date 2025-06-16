# 🤿 Scuba AI - Unfiltered and Unrestricted AI Assistant

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-green)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)](https://github.com/scuba25/Scuba-AI-unrestricted-ai)

A powerful, unfiltered AI assistant built with Flask and powered by Groq's LLaMA models. Scuba AI provides direct, comprehensive responses without typical AI restrictions or content filtering.

## ✨ Features

- **Unfiltered Responses**: No content restrictions or censorship
- **Modern UI**: Responsive design with mobile optimization
- **Real-time Chat**: Instant messaging with typing indicators
- **Conversation Memory**: Persistent chat history
- **Easy Deployment**: One-command installation script
- **PWA Ready**: Progressive Web App capabilities
- **API Integration**: Powered by Groq's advanced LLaMA models

## 🚀 Quick Start

### One-Command Installation

```bash
curl -fsSL https://raw.githubusercontent.com/scuba25/Scuba-AI-unrestricted-ai/main/install.sh | bash
```

### Manual Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/scuba25/Scuba-AI-unrestricted-ai.git
   cd Scuba-AI-unrestricted-ai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional)
   ```bash
   cp .env.example .env
   # Edit .env with your preferred settings
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your browser to `http://localhost:3000`

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# API Configuration
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=llama-3.1-8b-instant

# Server Configuration
PORT=3000
DEBUG=True
SECRET_KEY=your-secret-key-here

# Host Configuration (for production)
HOST=0.0.0.0
```

### API Key Setup

1. Get your free Groq API key from [console.groq.com](https://console.groq.com)
2. Replace the default key in `app.py` or set the `GROQ_API_KEY` environment variable

## 🛠️ System Requirements

- **Python**: 3.7 or higher
- **RAM**: 512MB minimum (1GB recommended)
- **Storage**: 100MB for application files
- **Network**: Internet connection for API calls

### Supported Operating Systems

- Ubuntu 16.04+
- CentOS 7+
- Arch Linux
- macOS 10.14+
- Windows 10+ (with WSL recommended)

## 📱 Usage

1. **Start a Conversation**: Type your message and press Enter
2. **Clear History**: Click the "Clear" button to start fresh
3. **Mobile Access**: Fully responsive design works on all devices
4. **PWA Installation**: Install as an app on mobile devices

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment

#### Using the included scripts:
```bash
# Start in production mode
./start-production.sh

# Update application
./update.sh
```

#### Manual production setup:
```bash
# Install production server
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:3000 app:app
```

#### Docker Deployment:
```bash
# Build the image
docker build -t scuba-ai .

# Run the container
docker run -p 3000:3000 -e GROQ_API_KEY=your_key_here scuba-ai
```

## 🔧 Advanced Configuration

### Custom Models

Scuba AI supports various Groq models:
- `llama-3.1-8b-instant` (default)
- `llama-3.1-70b-versatile`
- `mixtral-8x7b-32768`

Change the model in your `.env` file:
```env
MODEL_NAME=llama-3.1-70b-versatile
```

### Performance Tuning

For high-traffic deployments:

1. **Increase worker processes**:
   ```bash
   gunicorn -w 8 -b 0.0.0.0:3000 app:app
   ```

2. **Add Redis for session storage** (optional):
   ```bash
   pip install redis flask-session
   ```

3. **Configure reverse proxy** (Nginx example):
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:3000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

## 🔍 Troubleshooting

### Common Issues

**Application won't start:**
- Check if port 3000 is available: `lsof -i :3000`
- Verify Python version: `python --version`
- Install missing dependencies: `pip install -r requirements.txt`

**API errors:**
- Verify your Groq API key is valid
- Check internet connection
- Monitor API rate limits

**UI issues:**
- Clear browser cache
- Disable browser extensions
- Check console for JavaScript errors

### Debug Mode

Enable debug mode for detailed error information:
```bash
export DEBUG=True
python app.py
```

### Logs

Application logs are printed to the console. For production, redirect to a file:
```bash
python app.py > app.log 2>&1
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Include error handling

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔒 Security

For security issues, please email [security@scubaaai.info](mailto:security@scubaaai.info) instead of creating a public issue.

See [SECURITY.md](SECURITY.md) for our security policy.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/scuba25/Scuba-AI-unrestricted-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/scuba25/Scuba-AI-unrestricted-ai/discussions)
- **Website**: [scubaaai.info](https://scubaaai.info)

## 🙏 Acknowledgments

- [Groq](https://groq.com) for providing the AI models
- [Flask](https://flask.palletsprojects.com/) for the web framework
- The open-source community for various tools and libraries

---

**⚠️ Disclaimer**: Scuba AI is designed for research and educational purposes. Users are responsible for the ethical use of this technology. The developers do not endorse or encourage any misuse of the AI system.