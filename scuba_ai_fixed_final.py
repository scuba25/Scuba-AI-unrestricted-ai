from flask import Flask, render_template_string, request, jsonify, session
import requests
import json
import os
from datetime import datetime, timedelta
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Configuration
GROQ_API_KEY = "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"
MODEL_NAME = "llama-3.1-8b-instant"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

CONVERSATIONS_FILE = 'conversations.json'

def load_conversations():
    """Load conversations from file"""
    try:
        if os.path.exists(CONVERSATIONS_FILE):
            with open(CONVERSATIONS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Validate and clean conversation data
                cleaned_data = {}
                for conv_id, conv_data in data.items():
                    if isinstance(conv_data, dict) and 'messages' in conv_data:
                        # Ensure consistent key naming
                        if 'last_active' in conv_data:
                            conv_data['last_activity'] = conv_data.pop('last_active')
                        elif 'last_activity' not in conv_data:
                            conv_data['last_activity'] = datetime.now().isoformat()
                        
                        # Validate messages structure
                        valid_messages = []
                        for msg in conv_data.get('messages', []):
                            if isinstance(msg, dict) and 'role' in msg and 'content' in msg:
                                valid_messages.append(msg)
                        conv_data['messages'] = valid_messages
                        cleaned_data[conv_id] = conv_data
                return cleaned_data
        return {}
    except Exception as e:
        print(f"Error loading conversations: {e}")
        return {}

def save_conversations(conversations):
    """Save conversations to file"""
    try:
        with open(CONVERSATIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(conversations, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving conversations: {e}")

def cleanup_old_conversations():
    """Remove conversations older than 7 days"""
    try:
        conversations = load_conversations()
        cutoff_date = datetime.now() - timedelta(days=7)
        
        conversations_to_remove = []
        for conv_id, conv_data in conversations.items():
            try:
                last_activity_str = conv_data.get('last_activity', '')
                if last_activity_str:
                    # Handle different date formats
                    try:
                        last_activity = datetime.fromisoformat(last_activity_str.replace('Z', '+00:00'))
                    except:
                        try:
                            last_activity = datetime.strptime(last_activity_str, '%Y-%m-%d %H:%M:%S')
                        except:
                            # If we can't parse the date, assume it's old
                            last_activity = cutoff_date - timedelta(days=1)
                    
                    if last_activity < cutoff_date:
                        conversations_to_remove.append(conv_id)
                else:
                    # No timestamp, assume old
                    conversations_to_remove.append(conv_id)
            except Exception as e:
                print(f"Error processing conversation {conv_id}: {e}")
                conversations_to_remove.append(conv_id)
        
        for conv_id in conversations_to_remove:
            del conversations[conv_id]
        
        if conversations_to_remove:
            save_conversations(conversations)
            print(f"Cleaned up {len(conversations_to_remove)} old conversations")
    except Exception as e:
        print(f"Error during cleanup: {e}")

@app.route('/')
def index():
    """Main page"""
    cleanup_old_conversations()
    
    if 'conversation_id' not in session:
        session['conversation_id'] = str(uuid.uuid4())
    
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Scuba AI - Unfiltered and Unrestricted</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Segoe+UI:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
            overflow-x: hidden;
        }

        .header {
            background: linear-gradient(45deg, #007bff, #0056b3);
            color: white;
            padding: 15px 20px;
            text-align: center;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }

        .header h1 {
            font-family: 'Orbitron', monospace;
            font-size: 48px;
            font-weight: 900;
            color: #ffffff;
            text-shadow: 0 4px 8px rgba(0, 0, 0, 0.8);
            letter-spacing: 2px;
            margin-bottom: 5px;
        }

        .header .subtitle {
            font-size: 18px;
            font-weight: 500;
            color: #ffffff;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.6);
            margin-top: 0;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            height: 100vh;
            display: flex;
            flex-direction: column;
            padding: 0 15px;
        }

        .chat-area {
            flex: 1;
            padding: 120px 0 80px 0;
            overflow-y: auto;
            position: relative;
        }

        .welcome-message {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            color: white;
            font-size: 24px;
            font-weight: 500;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.6);
            transition: opacity 0.3s ease;
        }

        .welcome-message.hidden {
            opacity: 0;
            pointer-events: none;
        }

        .messages {
            display: none;
        }

        .messages.visible {
            display: block;
        }

        .message {
            margin-bottom: 20px;
            animation: fadeIn 0.3s ease-out;
        }

        .message-header {
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 5px;
            color: #007bff;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
        }

        .message-bubble {
            background: white;
            padding: 15px 20px;
            border-radius: 20px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            position: relative;
        }

        .user-message {
            text-align: right;
        }

        .user-message .message-bubble {
            background: linear-gradient(45deg, #007bff, #0056b3);
            color: white;
            margin-left: 20%;
        }

        .ai-message .message-bubble {
            background: white;
            color: #333;
            margin-right: 20%;
        }

        .input-area {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(45deg, #007bff, #0056b3);
            padding: 15px;
            box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.3);
        }

        .input-container {
            max-width: 800px;
            margin: 0 auto;
            display: flex;
            gap: 10px;
            align-items: center;
        }

        .welcome-above-input {
            position: absolute;
            bottom: 80px;
            left: 50%;
            transform: translateX(-50%);
            text-align: center;
            color: white;
            font-size: 20px;
            font-weight: 500;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.6);
            transition: opacity 0.3s ease;
            white-space: nowrap;
        }

        .welcome-above-input.hidden {
            opacity: 0;
            pointer-events: none;
        }

        #messageInput {
            flex: 1;
            padding: 12px 16px;
            border: none;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
            background: white;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
        }

        #sendButton {
            background: linear-gradient(45deg, #28a745, #20c997);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 25px;
            cursor: pointer;
            font-weight: 600;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
            transition: all 0.3s ease;
        }

        #sendButton:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        }

        #sendButton:disabled {
            background: #6c757d;
            cursor: not-allowed;
            transform: none;
        }

        .typing-indicator {
            display: none;
            margin-bottom: 20px;
        }

        .typing-indicator .message-bubble {
            background: white;
            color: #666;
            margin-right: 20%;
            font-style: italic;
        }

        .clear-button {
            background: linear-gradient(45deg, #dc3545, #c82333);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 14px;
            margin-left: 10px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
            transition: all 0.3s ease;
        }

        .clear-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Mobile Responsive */
        @media (max-width: 768px) {
            .header h1 {
                font-size: 36px;
            }
            
            .header .subtitle {
                font-size: 16px;
            }
            
            .welcome-message {
                font-size: 18px;
                padding: 0 20px;
            }
            
            .welcome-above-input {
                font-size: 18px;
                bottom: 85px;
            }
        }

        @media (max-width: 480px) {
            .header {
                padding: 12px 15px;
            }
            
            .header h1 {
                font-size: 32px;
            }
            
            .header .subtitle {
                font-size: 15px;
            }
            
            .chat-area {
                padding: 100px 0 80px 0;
            }
            
            .welcome-message {
                font-size: 16px;
            }
            
            .welcome-above-input {
                font-size: 16px;
                bottom: 85px;
            }
            
            .message-bubble {
                padding: 12px 16px;
            }
            
            .user-message .message-bubble {
                margin-left: 10%;
            }
            
            .ai-message .message-bubble {
                margin-right: 10%;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>SCUBA AI !</h1>
        <div class="subtitle">Unfiltered and Unrestricted</div>
    </div>

    <div class="container">
        <div class="chat-area">
            <div class="welcome-message" id="welcomeMessage">Welcome to Scuba AI !</div>
            
            <div class="messages" id="messages">
                <!-- Messages will be added here -->
            </div>
            
            <div class="typing-indicator" id="typingIndicator">
                <div class="message-header">Scuba AI</div>
                <div class="message-bubble">Thinking...</div>
            </div>
        </div>
    </div>

    <div class="welcome-above-input" id="welcomeAboveInput">Welcome to Scuba AI !</div>

    <div class="input-area">
        <div class="input-container">
            <input type="text" id="messageInput" placeholder="Type your message..." autocomplete="off">
            <button id="sendButton">Send</button>
            <button class="clear-button" onclick="clearChat()">Clear</button>
        </div>
    </div>

    <script>
        let conversationStarted = false;

        document.addEventListener('DOMContentLoaded', function() {
            const messageInput = document.getElementById('messageInput');
            const sendButton = document.getElementById('sendButton');
            const messagesContainer = document.getElementById('messages');
            const welcomeMessage = document.getElementById('welcomeMessage');
            const welcomeAboveInput = document.getElementById('welcomeAboveInput');
            const typingIndicator = document.getElementById('typingIndicator');

            // Focus on input when page loads
            setTimeout(() => {
                if (messageInput) {
                    messageInput.focus();
                }
            }, 100);

            // Send message function
            function sendMessage() {
                const message = messageInput.value.trim();
                if (!message || sendButton.disabled) return;

                // Hide welcome messages and show chat
                if (!conversationStarted) {
                    welcomeMessage.classList.add('hidden');
                    welcomeAboveInput.classList.add('hidden');
                    messagesContainer.classList.add('visible');
                    conversationStarted = true;
                }

                // Add user message
                addMessage('User', message, 'user');
                messageInput.value = '';
                sendButton.disabled = true;
                
                // Show typing indicator
                typingIndicator.style.display = 'block';

                // Send to backend
                fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                })
                .then(response => response.json())
                .then(data => {
                    typingIndicator.style.display = 'none';
                    if (data.response) {
                        addMessage('Scuba AI', data.response, 'ai');
                    } else {
                        addMessage('Scuba AI', 'Sorry, I encountered an error. Please try again.', 'ai');
                    }
                })
                .catch(error => {
                    typingIndicator.style.display = 'none';
                    console.error('Error:', error);
                    addMessage('Scuba AI', 'Sorry, I encountered an error. Please try again.', 'ai');
                })
                .finally(() => {
                    sendButton.disabled = false;
                    messageInput.focus();
                });
            }

            // Add message to chat
            function addMessage(sender, content, type) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${type}-message`;
                messageDiv.innerHTML = `
                    <div class="message-header">${sender}</div>
                    <div class="message-bubble">${content}</div>
                `;
                messagesContainer.appendChild(messageDiv);
                messageDiv.scrollIntoView({ behavior: 'smooth' });
            }

            // Event listeners
            sendButton.addEventListener('click', sendMessage);
            messageInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                }
            });

            // Global functions
            window.addMessage = addMessage;
            window.clearChat = function() {
                fetch('/clear', { method: 'POST' })
                .then(() => {
                    messagesContainer.innerHTML = '';
                    messagesContainer.classList.remove('visible');
                    welcomeMessage.classList.remove('hidden');
                    welcomeAboveInput.classList.remove('hidden');
                    conversationStarted = false;
                    messageInput.focus();
                });
            };
        });
    </script>
</body>
</html>
    ''')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        conversation_id = session.get('conversation_id')
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
            session['conversation_id'] = conversation_id
        
        # Load conversations
        conversations = load_conversations()
        
        # Get or create conversation
        if conversation_id not in conversations:
            conversations[conversation_id] = {
                'messages': [],
                'created': datetime.now().isoformat(),
                'last_activity': datetime.now().isoformat()
            }
        
        conversation = conversations[conversation_id]
        
        # Add user message
        conversation['messages'].append({
            'role': 'user',
            'content': user_message
        })
        
        # Prepare messages for API (only include valid messages)
        api_messages = []
        for msg in conversation['messages']:
            if isinstance(msg, dict) and 'role' in msg and 'content' in msg:
                api_messages.append({
                    'role': msg['role'],
                    'content': msg['content']
                })
        
        # Call Groq API
        headers = {
            'Authorization': f'Bearer {GROQ_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': MODEL_NAME,
            'messages': api_messages,
            'max_tokens': 1000,
            'temperature': 0.7
        }
        
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            response_data = response.json()
            ai_response = response_data['choices'][0]['message']['content']
            
            # Add AI response to conversation
            conversation['messages'].append({
                'role': 'assistant',
                'content': ai_response
            })
            
            # Update last activity
            conversation['last_activity'] = datetime.now().isoformat()
            
            # Save conversations
            save_conversations(conversations)
            
            return jsonify({'response': ai_response})
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return jsonify({'error': 'API request failed'}), 500
            
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/clear', methods=['POST'])
def clear_chat():
    """Clear current conversation"""
    try:
        conversation_id = session.get('conversation_id')
        if conversation_id:
            conversations = load_conversations()
            if conversation_id in conversations:
                del conversations[conversation_id]
                save_conversations(conversations)
        
        # Create new conversation ID
        session['conversation_id'] = str(uuid.uuid4())
        return jsonify({'success': True})
    except Exception as e:
        print(f"Clear chat error: {e}")
        return jsonify({'error': 'Failed to clear chat'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)