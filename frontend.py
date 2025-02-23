import streamlit as st
import requests
from datetime import datetime
import base64

import os


BASE_URL = os.getenv("BACKEND_URL", "http://backend:8000")
st.set_page_config(page_title="IT Visionary Chat Assistant", page_icon="🤖")


def initialize_session():
    """Create a new chat session"""
    response = requests.post(f"{BASE_URL}/api/start")
    if response.status_code == 200:
        data = response.json()
        return data['session_id'], data['assistant_response']
    else:
        st.error("Failed to initialize session")
        return None, None

def send_message(session_id, message):
    """Send message to backend and get response"""
    payload = {
        "session_id": session_id,
        "message": message
    }
    response = requests.post(f"{BASE_URL}/api/chat", json=payload)
    if response.status_code == 200:
        return response.json()['assistant_response']
    else:
        st.error(f"Error: {response.text}")
        return None


def add_header_with_image(image_path):
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    encoded_image = base64.b64encode(image_bytes).decode()
    
    st.markdown(
        f"""
        <style>
        .header-container {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            background-color: #0E1117;
        }}
        .header-image {{
            height: 70px;
            margin-left: 20px;
        }}
        </style>
        
        <div class="header-container">
            <h1 style='margin: 0;'>Chat Assistant</h1>
            <img class="header-image" src="data:image/png;base64,{encoded_image}">
        </div>
        """,
        unsafe_allow_html=True
    )

add_header_with_image("It_Visionary_logo.png")  


if 'session_id' not in st.session_state:
    st.session_state.session_id = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:
    st.header("Session Management")
    if st.button("New Chat Session"):
        session_id, response = initialize_session()
        if session_id:
            st.session_state.session_id = session_id
            st.session_state.chat_history = [("assistant", response)]
            st.rerun()

# Display chat history
chat_container = st.container()
with chat_container:
    for role, message in st.session_state.chat_history:
        if role == "user":
            with st.chat_message("user"):
                st.markdown(f"<div style='background-color:#0a0629; padding:10px; border-radius:10px; margin:5px 0;'>{message}</div>", unsafe_allow_html=True)
        else:
            with st.chat_message("assistant"):
                st.markdown(f"<div style='background-color:#0a0629; padding:10px; border-radius:10px; margin:5px 0;'>{message}</div>", unsafe_allow_html=True)

# input area
if st.session_state.session_id:
    user_input = st.chat_input("Type your message here...")
    if user_input:
        st.session_state.chat_history.append(("user", user_input))
        
        response = send_message(st.session_state.session_id, user_input)
        
        if response:
            st.session_state.chat_history.append(("assistant", response))
            st.rerun()
else:
    st.info("Please start a new chat session using the sidebar button.")