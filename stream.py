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
        return True  # Conservative fallback

def generate_with_gemini(prompt):
    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except:
        return "Sorry, I couldn't process your request at the moment."

# --- STREAMLIT UI ---
st.set_page_config(page_title="Smart Investment Chatbot", page_icon="💼", layout="centered")

st.title("💼 Smart Investment Chatbot")
st.caption("AI-powered investment insights")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
question = st.chat_input("Ask about investments...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # Determine response
    if is_greeting(question):
        response = "Hello! How can I assist you with your investments today?"
    elif not check_investment_intent(question):
        response = "Please ask investment-related questions only."
    else:
        response = generate_with_gemini(question)

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
