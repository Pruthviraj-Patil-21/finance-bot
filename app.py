# # import streamlit as st
# # import requests
# # import os
# # from dotenv import load_dotenv

# # # Load .env
# # load_dotenv()
# # GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# # # Page config
# # st.set_page_config(page_title="💰 FinChat - Your Money Buddy", page_icon="💸", layout="centered")

# # # Custom CSS for style
# # st.markdown("""
# #     <style>
# #     .user-bubble {
# #         background-color:rgb(180,180,180);
# #         padding: 10px;
# #         border-radius: 10px;
# #         margin-bottom: 10px;
# #         text-align: right;
# #     }
# #     .bot-bubble {
# #         background-color: #F1F0F0;
# #         padding: 10px;
# #         border-radius: 10px;
# #         margin-bottom: 10px;
# #         text-align: left;
# #     }
# #     .stTextInput>div>div>input {
# #         border: 2px solid #4CAF50;
# #         border-radius: 8px;
# #     }
# #     .stButton>button {
# #         background-color: #4CAF50;
# #         color: white;
# #         border-radius: 8px;
# #     }
# #     </style>
# # """, unsafe_allow_html=True)

# # # Title and description
# # st.title("💸 FinChat - Your Money Buddy")
# # st.markdown("Ask me about *saving, **investing, **budgeting*, or any financial term! Let's make money simple.")

# # # Chat history storage
# # if "chat_history" not in st.session_state:
# #     st.session_state.chat_history = []

# # # User input
# # question = st.text_input("💬 Type your financial question:")

# # if st.button("Ask") and question:
# #     # Add user message to chat
# #     st.session_state.chat_history.append(("user", question))

# #     # Show "thinking"
# #     with st.spinner("🤔 Thinking..."):

# #         headers = {
# #             "Authorization": f"Bearer {GROQ_API_KEY}",
# #             "Content-Type": "application/json"
# #         }

# #         data = {
# #             "model": "llama3-70b-8192",
# #             "messages": [
# #                 {"role": "system", "content": "You are a friendly and expert financial literacy assistant. Explain things clearly and simply."},
# #                 {"role": "user", "content": question}
# #             ]
# #         }

# #         response = requests.post(
# #             "https://api.groq.com/openai/v1/chat/completions",
# #             headers=headers,
# #             json=data
# #         )

# #         if response.status_code == 200:
# #             answer = response.json()['choices'][0]['message']['content']
# #             # Add bot reply to chat
# #             st.session_state.chat_history.append(("bot", answer))
# #         else:
# #             st.error(f"Error: {response.text}")

# # # Display chat bubbles
# # for role, message in st.session_state.chat_history:
# #     if role == "user":
# #         st.markdown(f"<div class='user-bubble'>🙋‍♂ {message}</div>", unsafe_allow_html=True)
# #     else:
# #         st.markdown(f"<div class='bot-bubble'>🤖 {message}</div>", unsafe_allow_html=True)

# import streamlit as st
# import requests
# import json
# import os
# from dotenv import load_dotenv

# # Load API Key
# load_dotenv()
# api_key = os.getenv("GROQ_API_KEY")

# # Function to call Groq API
# def chat_with_groq(prompt):
#     url = "https://api.groq.com/openai/v1/chat/completions"
#     headers = {
#         "Authorization": f"Bearer {api_key}",
#         "Content-Type": "application/json"
#     }
#     payload = {
#         "model": "llama3-70b-8192",
#         "messages": [
#             {"role": "user", "content": prompt}
#           ]
#     }
#     response = requests.post(url, headers=headers, data=json.dumps(payload))
#     if response.status_code == 200:
#         return response.json()['choices'][0]['message']['content']
#     else:
#         return "Error: " + str(response.text)

# # Streamlit page config
# st.set_page_config(page_title="Groq Chat", page_icon="🤖", layout="centered")

# #Custom CSS for styling
# st.markdown("""
#     <style>
#       body {
#        background-color: #1e1e1e;
#          color: white;
#        }
#      .stTextInput>div>div>input {
#      font-size: 20px;
#          padding: 15px;
#          border-radius: 10px;
#     }
#     .big-font {
#         font-size: 22px !important;
#      color: black;
#          background-color:whte;
#          padding-10px 24px;
#          border-radius:8px;
#          margin-top:20px;            

#      }
#      .stButton button {
#          font-size: 18px;
#          padding: 10px 24px;
#          border-radius: 8px;
#          background-color: #4CAF50;
#          color: white;
#          border: none;
#      }
#      .stButton button:hover {
#          background-color: #45a049;
#          color: white;
#      }
#     </style>
# """, unsafe_allow_html=True)


# # Title
# st.title("🤖 Chat with Groq AI")

# # Input
# user_input = st.text_input("Ask me anything:", "", key="input")

# # Stylish Button
# if st.button("✨ Ask"):
#     if user_input:
#         with st.spinner('Thinking...'):
#             answer = chat_with_groq(user_input)
#         st.markdown(f'<p class="big-font">{answer}</p>', unsafe_allow_html=True)

import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Load Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

# Initialize session state to store chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant who teaches financial literacy in simple words."}
    ]

# CSS Styling
st.markdown("""
    <style>
    body {
        background-color: #1e1e1e;
        color: white;
    }
    .stTextInput>div>div>input {
        font-size: 20px;
        padding: 15px;
        border-radius: 10px;
    }
    .user-bubble {
        background-color: #4CAF50;
        color: white;
        padding: 10px 15px;
        border-radius: 15px;
        margin: 10px 0;
        max-width: 80%;
        align-self: flex-end;
    }
    .bot-bubble {
        background-color: #2e2e2e;
        color: #f1f1f1;
        padding: 10px 15px;
        border-radius: 15px;
        margin: 10px 0;
        max-width: 80%;
        align-self: flex-start;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
    }
    .stButton button {
        font-size: 18px;
        padding: 10px 24px;
        border-radius: 8px;
        background-color: #4CAF50;
        color: white;
        border: none;
    }
    .stButton button:hover {
        background-color: #45a049;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='color: #00ffcc;'>💸 Financial Literacy Chatbot</h1>", unsafe_allow_html=True)

# Chat history display
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for msg in st.session_state.messages[1:]:  # Skip the system message
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f'<div class="bot-bubble">{msg["content"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Input box
prompt = st.text_input("Ask me about money, savings, investing...")

if st.button("Get Answer"):
    if prompt:
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Call Groq API with full history
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=st.session_state.messages
        )

        answer = response.choices[0].message.content

        # Add assistant message to history
        st.session_state.messages.append({"role": "assistant", "content": answer})

        # Rerun to display updated chat
        st.rerun()