import streamlit as st
import os
import pyttsx3
import pythoncom
import threading
from groq import Groq
from dotenv import load_dotenv
import speech_recognition as sr  # Added import for speech recognition

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("🚨 GROQ_API_KEY not found in .env file")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# Fix for COM init
pythoncom.CoInitialize()

# Global variables for speech engine
engine = pyttsx3.init()
stop_speaking_flag = threading.Event()
currently_speaking_text = ""

# Speak function using thread
def speak_async(text):
    global currently_speaking_text
    stop_speaking_flag.clear()
    currently_speaking_text = text

    def run():
        engine.say(text)
        engine.runAndWait()
        currently_speaking_text = ""

    t = threading.Thread(target=run)
    t.start()

# Stop speaking
def stop_speaking():
    stop_speaking_flag.set()
    engine.stop()

# Speech recognition function
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Listening... Speak now.")
        audio = r.listen(source, timeout=5, phrase_time_limit=10)
        try:
            text = r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            st.warning("Sorry, I couldn't understand that.")
        except sr.RequestError:
            st.error("Speech recognition service is unavailable.")
    return ""

# Session state init
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant who teaches financial literacy in simple words."}
    ]
if "prompt" not in st.session_state:
    st.session_state.prompt = ""
if "voice_enabled" not in st.session_state:
    st.session_state.voice_enabled = False
if "reading_text" not in st.session_state:
    st.session_state.reading_text = ""

# CSS
st.markdown("""
    <style>
    .title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        color: #004d66;
        margin-bottom: 30px;
    }
    .chat-container {
        background-color: white;
        border-radius: 12px;
        padding: 25px;
        max-height: 500px;
        overflow-y: auto;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .user-bubble {
        background-color: #d1e7dd;
        color: #0f5132;
        padding: 12px 18px;
        border-radius: 15px;
        margin: 10px 0;
        max-width: 75%;
        margin-left: auto;
        font-size: 16px;
        box-shadow: 1px 1px 5px rgba(0,0,0,0.1);
    }
    .bot-bubble {
        background-color: #e2e3e5;
        color: #41464b;
        padding: 12px 18px;
        border-radius: 15px;
        margin: 10px 0;
        max-width: 75%;
        margin-right: auto;
        font-size: 16px;
        box-shadow: 1px 1px 5px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<div class='title'>💸 Financial Literacy Chatbot</div>", unsafe_allow_html=True)

# Clear + voice toggle
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("🧹 Clear"):
        st.session_state.messages = [
            {"role": "system", "content": "You are a helpful assistant who teaches financial literacy in simple words."}
        ]
        st.session_state.prompt = ""
        st.session_state.reading_text = ""
        st.rerun()
with col2:
    st.session_state.voice_enabled = st.toggle("🎤 Voice Mode", value=st.session_state.voice_enabled)

# Chat history
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f'<div class="bot-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Speaking text display
if st.session_state.reading_text:
    st.info(f"🔊 Speaking: {st.session_state.reading_text}")

# Input area
col3, col4, col5, col6 = st.columns([3, 1, 1, 1])  # Unpacking into four variables
with col3:
    if st.session_state.voice_enabled:
        voice_input = recognize_speech()
        if voice_input:
            st.session_state.prompt = voice_input
    else:
        st.session_state.prompt = st.text_input("Ask me about money, saving, investing...", value=st.session_state.prompt)

with col4:
    if st.button("📤 Send"):
        prompt = st.session_state.prompt.strip()
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            try:
                response = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=st.session_state.messages
                )
                answer = response.choices[0].message.content  # Fixed the issue here
                st.session_state.messages.append({"role": "assistant", "content": answer})
                if st.session_state.voice_enabled:
                    st.session_state.reading_text = answer
                    speak_async(answer)
            except Exception as e:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "❗ Sorry, something went wrong."
                })
                st.error(f"Error: {e}")
            st.session_state.prompt = ""
            st.rerun()

# Removed the microphone button logic entirely
with col5:
    pass

# Keep the "Stop Voice" button if voice mode is enabled
with col6:
    if st.session_state.voice_enabled and st.button("⏹ Stop Voice"):
        stop_speaking()
        st.session_state.reading_text = ""
        st.rerun()

