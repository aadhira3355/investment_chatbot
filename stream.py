import streamlit as st
import google.generativeai as genai

# --- GEMINI SETUP ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
gemini_model = genai.GenerativeModel('models/gemini-2.0-flash-001')

# --- HELPER FUNCTIONS ---
def is_greeting(text):
    greetings = ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']
    return any(greet in text.lower().strip() for greet in greetings)

def check_investment_intent(question):
    prompt = (
        "Please answer with 'yes' or 'no' only. "
        "Is the following question related to investments, finance, stocks, bonds, "
        "mutual funds, or financial planning?\n\n"
        f"Question: \"{question}\""
    )
    try:
        response = gemini_model.generate_content(prompt)
        answer = response.text.strip().lower()
        return 'yes' in answer
    except:
        return True

def generate_with_gemini(prompt):
    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except:
        return "Sorry, I couldn't process your request at the moment."

# --- PAGE CONFIG ---
st.set_page_config(page_title="Smart Investment Chatbot", page_icon="📈", layout="centered")

# --- CUSTOM CSS STYLE ---
st.markdown("""
    <style>
    .stApp {
        background-color: #121e2c;
        color: #f0f0f0;
        font-family: 'Segoe UI', sans-serif;
    }
    .block-container {
        padding-top: 2rem;
        max-width: 850px;
        margin: auto;
    }
    h1, h2, h3, h4, h5, h6, .stMarkdown {
        color: #f0f0f0;
    }
    .stChatMessage {
        font-size: 22px;
        line-height: 1.75;
    }
    .stChatMessage.user {
        background: linear-gradient(to right, #324960, #3e5a77);
        color: white;
        border-radius: 16px 16px 6px 16px;
        padding: 12px 18px;
    }
    .stChatMessage.assistant {
        background: #e9f1fc;
        color: #1b2a3b;
        border-radius: 16px 16px 16px 6px;
        padding: 12px 18px;
    }
    div[role="textbox"] textarea {
        font-size: 20px !important;
        background-color: #2a3c50 !important;
        color: white !important;
        border-radius: 8px;
        border: 1.5px solid #6c8ca1;
        padding: 10px;
    }
    img {
        border-radius: 14px;
        margin-bottom: 10px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.25);
    }
    </style>
""", unsafe_allow_html=True)

# --- IMAGE HEADER ---
st.image("img1.jpg", use_container_width=True, caption="💡 Smart Investment Assistant", output_format='auto')

# --- HEADER TEXT ---
st.markdown("<h1 style='text-align:center; font-size: 36px;'>📈 Smart Investment Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center; color:#a3c9f9;'>Get investment insights instantly using AI</h4>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:18px;'>💬 Try: <em>Compare stocks vs gold</em> or <em>Best long-term investment</em></p>", unsafe_allow_html=True)

# --- CHATBOT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
question = st.chat_input("Ask your investment question...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    if is_greeting(question):
        response = "👋 Hello! How can I help you with your investment questions today?"
    elif not check_investment_intent(question):
        response = "⚠️ Please ask investment-related questions only."
    else:
        response = generate_with_gemini(question)

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
