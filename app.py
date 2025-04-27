import streamlit as st
import os
import requests
from dotenv import load_dotenv
import uuid
from bias_detection import BiasDetector
from data_integration import DataIntegrator
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import time

# Custom CSS for animations and styling
st.markdown("""
<style>
    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(20px);}
        to {opacity: 1; transform: translateY(0);}
    }
    
    @keyframes pulse {
        0% {transform: scale(1);}
        50% {transform: scale(1.05);}
        100% {transform: scale(1);}
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .main-header {
        animation: fadeIn 1s ease-out;
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .chat-message {
        animation: fadeIn 0.5s ease-out;
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        color: #333;
        font-size: 1rem;
        line-height: 1.5;
    }
    
    .user-message {
        background: #e3f2fd;
        margin-left: 20%;
        color: #1a237e;
    }
    
    .assistant-message {
        background: #f5f5f5;
        margin-right: 20%;
        color: #333;
    }
    
    .bias-warning {
        animation: pulse 1s infinite;
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        color: #856404;
    }
    
    .positive-reinforcement {
        background: #d4edda;
        border-left: 4px solid #28a745;
        color: #155724;
    }
    
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(0,0,0,.1);
        border-radius: 50%;
        border-top-color: #667eea;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Input box styling */
    .stTextInput>div>div>input {
        background-color: white;
        border-radius: 15px;
        padding: 12px;
        font-size: 1rem;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    
    .stTextInput>div>div>input::placeholder {
        color: #999;
    }
    
    /* Chat container styling */
    .stChatMessage {
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    /* Ensure text visibility in all states */
    .stMarkdown {
        color: #333;
    }
    
    .stJson {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 1rem;
        border-radius: 10px;
        margin-top: 0.5rem;
    }
    
    /* Fix for dark mode text visibility */
    @media (prefers-color-scheme: dark) {
        .chat-message {
            color: #fff;
        }
        .user-message {
            color: #e3f2fd;
        }
        .assistant-message {
            color: #f5f5f5;
        }
        .stMarkdown {
            color: #fff;
        }
        .assistant-message {
            background: #222;
            color: #fff;
        }
        .user-message {
            background: #333;
            color: #fff;
        }
    }
</style>
""", unsafe_allow_html=True)

# Load environment variables
# load_dotenv()

# Configure Groq API
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
if not GROQ_API_KEY:
    st.error("GROQ_API_KEY environment variable is not set")
    st.stop()

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"

def call_groq_llama33(message: str, history=None):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant for women's career development and empowerment."},
            *(history or []),
            {"role": "user", "content": message}
        ],
        "max_tokens": 512,
        "temperature": 0.7
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

# Initialize services
bias_detector = BiasDetector()
data_integrator = DataIntegrator()

# Initialize session state for conversation history
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'conversation_id' not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())

def extract_search_queries(message: str):
    """Extract search queries from the message"""
    queries = {}
    keywords = {
        'jobs': ['job', 'career', 'position', 'role', 'work'],
        'events': ['event', 'meetup', 'conference', 'workshop', 'session'],
        'mentorship': ['mentor', 'mentorship', 'guidance', 'coach']
    }
    message_lower = message.lower()
    for category, words in keywords.items():
        for word in words:
            if word in message_lower:
                parts = message_lower.split(word, 1)
                if len(parts) > 1:
                    queries[category] = parts[1].strip()
                    break
    return queries

def get_chat_response(message: str):
    """Get response from the chatbot"""
    try:
        # Check for bias in user message
        has_bias, detected_patterns = bias_detector.detect_bias(message)
        is_positive = bias_detector.check_positive_reinforcement(message)
        
        # Extract search queries and get relevant data
        queries = extract_search_queries(message)
        data_results = {}
        if 'jobs' in queries:
            data_results['jobs'] = data_integrator.search_jobs(queries['jobs'])
        if 'events' in queries:
            data_results['events'] = data_integrator.search_events(queries['events'])
        if 'mentorship' in queries:
            data_results['mentorship'] = data_integrator.get_mentorship_programs()
        
        # Prepare chat history for context
        history = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.conversation_history if m["role"] in ("user", "assistant")
        ]
        
        # Generate response using Groq Llama 3.3
        response_text = call_groq_llama33(message, history)
        
        # Check for bias in AI response
        response_has_bias, response_patterns = bias_detector.detect_bias(response_text)
        response_is_positive = bias_detector.check_positive_reinforcement(response_text)
        
        # If bias is detected, suggest mitigation
        if response_has_bias:
            mitigated_response = bias_detector.suggest_mitigation(response_text)
            response_text = mitigated_response
        
        return {
            "response": response_text,
            "has_bias": has_bias or response_has_bias,
            "detected_patterns": detected_patterns + response_patterns,
            "is_positive": is_positive or response_is_positive,
            "data_results": data_results if data_results else None
        }
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# Streamlit UI
st.markdown('<div class="main-header"><h1>Asha AI Chatbot</h1></div>', unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; margin-bottom: 2rem;'>
    <p style='font-size: 1.2rem; color: #666;'>
        Your virtual assistant for women's career development and empowerment
    </p>
</div>
""", unsafe_allow_html=True)

# Display conversation history
for message in st.session_state.conversation_history:
    message_class = "user-message" if message["role"] == "user" else "assistant-message"
    additional_classes = []
    if message.get("has_bias"):
        additional_classes.append("bias-warning")
    if message.get("is_positive"):
        additional_classes.append("positive-reinforcement")
    
    with st.chat_message(message["role"]):
        st.markdown(f'<div class="chat-message {message_class} {" ".join(additional_classes)}">{message["content"]}</div>', unsafe_allow_html=True)
        if message.get("data_results"):
            st.json(message["data_results"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat
    with st.chat_message("user"):
        st.markdown(f'<div class="chat-message user-message">{prompt}</div>', unsafe_allow_html=True)
    
    # Get and display assistant response
    with st.chat_message("assistant"):
        # Show loading animation
        loading_placeholder = st.empty()
        loading_placeholder.markdown('<div class="loading"></div>', unsafe_allow_html=True)
        
        # Get response
        response = get_chat_response(prompt)
        
        # Clear loading animation
        loading_placeholder.empty()
        
        if response:
            # Add classes based on response properties
            response_classes = ["chat-message", "assistant-message"]
            if response["has_bias"]:
                response_classes.append("bias-warning")
            if response["is_positive"]:
                response_classes.append("positive-reinforcement")
            
            st.markdown(f'<div class="{" ".join(response_classes)}">{response["response"]}</div>', unsafe_allow_html=True)
            
            if response["data_results"]:
                st.json(response["data_results"])
            
            # Update conversation history
            st.session_state.conversation_history.append({
                "role": "user",
                "content": prompt
            })
            st.session_state.conversation_history.append({
                "role": "assistant",
                "content": response["response"],
                "has_bias": response["has_bias"],
                "is_positive": response["is_positive"],
                "data_results": response["data_results"]
            }) 