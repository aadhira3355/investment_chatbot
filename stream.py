import streamlit as st
import google.generativeai as genai

# Configure the Gemini API with the secret
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

# --- STREAMLIT UI CONFIG ---
st.set_page_config(page_title="Smart Investment Chatbot", page_icon="📈", layout="centered")

# --- CUSTOM FONT AND STYLING ---
st.markdown("""
    <style>
    .stApp {
        background-color: #1e2a38;
        color: #ffffff;
        font-family: 'Segoe UI', sans-serif;
        font-size: 50px;
    }
    .stChatMessage {
        font-size: 50px;
        line-height: 1.65;
    }
    div[role="textbox"] textarea {
        font-size: 100px !important;
        color: white !important;
        background-color: #3b4a5a !important;
        border-radius: 8px;
        border: 1.5px solid #8899aa;
    }
    </style>
""", unsafe_allow_html=True)

# --- IMAGE HEADER ---
st.image("img1.jpg", use_container_width=True, caption="Smart Investment Assistant", output_format='auto')

# --- HEADER ---
st.title("📈 Smart Investment Chatbot")
st.markdown("#### AI-powered investment insights")
st.caption("💡 Try questions like: *'Best long-term investment?'* or *'Compare mutual funds and stocks'*")

# --- CHAT FUNCTIONALITY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

question = st.chat_input("Ask about investments...")

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
