# ================================
# app.py - Main Application File
# ================================

from flask import Flask, render_template_string, request, jsonify, session
import requests
import json
import os
from datetime import datetime, timedelta
import uuid

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production')

# Configuration
GROQ_API_KEY = os.getenv('GROQ_API_KEY', "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")
MODEL_NAME = os.getenv('MODEL_NAME', "llama-3.1-8b-instant")
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
            right