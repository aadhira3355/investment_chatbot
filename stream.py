import streamlit as st
import time
import google.generativeai as genai

# --- GEMINI SETUP ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
gemini_model = genai.GenerativeModel('models/gemini-2.0-flash-001')

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

# --- CUSTOM CSS STYLING ---
st.markdown("""
    <style>
    .stApp {
        background-color: #101d2c;
        color: #f0f0f0;
        font-family: 'Segoe UI', sans-serif;
    }
    .block-container {
        padding-top: 2rem;
        max-width: 850px;
        margin: auto;
    }
    h1 {
        animation: bounce 1s ease;
        font-size: 38px;
        text-align: center;
        color: #a3d0f9;
    }
    @keyframes bounce {
        0% { transform: scale(0.95); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    .stChatMessage {
        font-size: 22px;
        line-height: 1.75;
        animation: fadeIn 0.5s ease-in;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stChatMessage.user {
        background: linear-gradient(to right, #344a5e, #456179);
        color: white;
        border-radius: 16px 16px 6px 16px;
        padding: 12px 18px;
    }
    .stChatMessage.assistant {
        background: #f4f9ff;
        color: #1b2a3b;
        border-radius: 16px 16px 16px 6px;
        padding: 12px 18px;
    }
    div[role="textbox"] textarea {
        font-size: 20px !important;
        background-color: #2a3c50 !important;
        color: white !important;
        border: 1.5px solid #6c8ca1;
        border-radius: 8px;
        padding: 10px;
    }
    img {
        border-radius: 14px;
        margin-bottom: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.25);
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER IMAGE ---
st.image("img1.jpg", use_container_width=True)

# --- HEADER TEXT ---
st.markdown("<h1>📈 Smart Investment Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center; color:#a3c9f9;'>Your AI assistant for smarter financial decisions</h4>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:18px;'>💬 Try: <em>‘Best long-term investment?’</em> or <em>‘Compare ETFs and gold’</em></p>", unsafe_allow_html=True)

# --- CHAT STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- DISPLAY CHAT HISTORY ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- CHAT INPUT ---
question = st.chat_input("Ask your investment question...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # Show typing animation
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            time.sleep(1)  # Simulated delay

            if is_greeting(question):
                response = "👋 Hello! How can I help you with your investment questions today?"
            elif not check_investment_intent(question):
                response = "⚠️ Please ask investment-related questions only."
            else:
                response = generate_with_gemini(question)

            # Typing animation
            placeholder = st.empty()
            animated_text = ""
            for char in response:
                animated_text += char
                placeholder.markdown(animated_text)
                time.sleep(0.01)  # typing effect

    st.session_state.messages.append({"role": "assistant", "content": response})
