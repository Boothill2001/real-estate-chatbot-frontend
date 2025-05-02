# app_frontend.py – Real Estate Chatbot (Final Full Pack with Reasoning Trace + Search Time)

import streamlit as st
import requests
import time

# 🎨 Inject Custom CSS + Bootstrap Icons
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 🚀 Page Setup
st.set_page_config(page_title="🏡 Real Estate Chatbot", layout="wide")

local_css("custom_theme.css")
st.markdown("""
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">
""", unsafe_allow_html=True)

st.title("🏡 Real Estate Chatbot via API")
st.caption("⚡ Powered by FastAPI + Streamlit + Bootstrap Icons")

# 📚 Suggested Questions
suggested_questions = [
    "Find affordable 4-room flats in Yishun under 400k SGD",
    "List 5-room flats in Bukit Batok priced below 600k SGD",
    "Are there any executive flats in Pasir Ris under 800k SGD",
    "Flats with lease start after 2015 in Sengkang",
    "What's the average price for 3-room flats in Ang Mo Kio?"
]

# 🔥 Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "is_bot_typing" not in st.session_state:
    st.session_state.is_bot_typing = False

# 🛠️ Sidebar Settings
with st.sidebar:
    st.header("⚙️ Settings")
    top_k = st.slider("📊 Number of results", min_value=3, max_value=10, value=5)
    if st.button("🧹 Clear Chat History"):
        st.session_state.chat_history = []
        st.experimental_rerun()

st.subheader("🔍 Suggested Questions:")
cols = st.columns(2)
for i, q in enumerate(suggested_questions):
    if cols[i % 2].button(q):
        st.session_state.user_input = q

# 💬 Input
user_input = st.text_input(
    "💬 Ask your real estate question:",
    value=st.session_state.get("user_input", ""),
    placeholder="e.g. Find 4-room flats in Woodlands under 400k SGD"
)

# 🚀 API Endpoint
API_URL = "https://real-estate-rag-backend-520862369717.asia-southeast1.run.app/ask"

# 👉 Send Query
if st.button("🚀 Ask Now"):
    if user_input.strip():
        st.session_state.is_bot_typing = True
        with st.spinner("⏳ Sending your query to backend..."):
            try:
                payload = {"query": user_input, "top_k": top_k}
                st.session_state.start_time = time.time()  # ⏱️ Record start time
                res = requests.post(API_URL, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    search_time = round(time.time() - st.session_state.start_time, 2)
                    st.session_state.chat_history.append(
                        (user_input, data.get('documents', []), data.get('plan_steps', []), search_time)
                    )
                else:
                    st.session_state.chat_history.append((user_input, f"❌ Error {res.status_code}: {res.text}", [], 0))
            except Exception as e:
                st.session_state.chat_history.append((user_input, f"❌ Exception: {str(e)}", [], 0))
            st.session_state.user_input = ""
        st.session_state.is_bot_typing = False
        time.sleep(0.5)
        st.rerun()

# 💬 Display Chat with Bubble + Bootstrap Icon + Reasoning Trace + Search Time
for user_msg, bot_docs, reasoning_steps, search_time in st.session_state.chat_history:
    with st.container():
        with st.chat_message("user"):
            st.markdown(f"""
                <div class='chat-bubble-user'>
                    <i class="bi bi-person-circle"></i> {user_msg}
                </div>
            """, unsafe_allow_html=True)

        with st.chat_message("assistant"):
            if isinstance(bot_docs, list):
                for i, doc in enumerate(bot_docs, 1):
                    st.markdown(f"""
                        <div class='chat-bubble-bot'>
                            <i class="bi bi-robot"></i> <strong>Result {i}:</strong><br>{doc}
                        </div><br>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class='chat-bubble-bot'>
                        <i class="bi bi-robot"></i> {bot_docs}
                    </div>
                """, unsafe_allow_html=True)

            # ✨ Reasoning Trace
            if reasoning_steps:
                st.markdown(f"""
                    <div class='chat-reasoning-trace'>
                        <i class="bi bi-lightbulb"></i> <strong>Agent Reasoning:</strong> {" ➔ ".join(reasoning_steps)}
                    </div>
                """, unsafe_allow_html=True)

            # ✨ Search Time
            if search_time:
                st.markdown(f"""
                    <div class='chat-search-time'>
                        <i class="bi bi-clock"></i> <em>Search completed in {search_time} seconds.</em>
                    </div>
                """, unsafe_allow_html=True)

# ✨ Typing Animation
if st.session_state.is_bot_typing:
    with st.chat_message("assistant"):
        st.markdown("""
            <div class='chat-bubble-bot'>
                <i class="bi bi-robot"></i> Typing...
            </div>
        """, unsafe_allow_html=True)

# 📜 Footer
st.markdown("---")
st.caption("© 2025 Real Estate RAG Chatbot - Powered by FastAPI + Streamlit + Bootstrap Icons")
