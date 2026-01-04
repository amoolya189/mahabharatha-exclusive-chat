# app.py
import streamlit as st
from qa import answer_question

# ============================
# Streamlit Page Configuration
# ============================
st.set_page_config(
    page_title="Mahabharata GPT",
    page_icon="🕉️",
    layout="centered"
)

# ============================
# Session State Initialization
# ============================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

# ============================
# Custom CSS
# ============================
page_bg_img = """
<style>
.stApp {
    background-image: url("https://thumbs.dreamstime.com/b/mahabharata-silhouette-symbol-icon-great-hindu-mythology-96933694.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

.stApp::before {
    content: "";
    position: absolute;
    inset: 0;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: -1;
}

h1, h2, h3, h4, h5, h6, p, label, span, div {
    color: #000000 !important;
    font-weight: bold !important;
    font-family: 'Lucida Calligraphy', serif;
}

.stTextInput>div>input {
    background-color: #000000 !important;
    color: #FFFFFF !important;
    font-weight: bold !important;
    border: 2px solid #FFFFFF !important;
}

.stButton>button {
    background-color: #FFD700;
    color: black;
    font-weight: bold;
    width: 100%;
    border: 2px solid #000000;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# ============================
# App Header
# ============================
st.title("🕉️ Mahabharata GPT - Ask Anything!")

st.markdown(
    "<p style='text-align: center; font-size:18px;'>Ask any question about the Mahabharata and get a detailed, scholarly answer.</p>",
    unsafe_allow_html=True
)

# ============================
# Display Chat History
# ============================
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown("### 🧑 You")
        st.markdown(msg["content"])
    else:
        st.markdown("### 🕉️ Mahabharata GPT")
        st.markdown(msg["content"])

st.markdown("---")

# ============================
# Question Input (FORM)
# ============================
with st.form(key="question_form", clear_on_submit=True):
    question = st.text_input("Your Question:")
    submit = st.form_submit_button("Ask")

# ============================
# Handle New Question (Phase 1)
# ============================
if submit and question.strip():
    # Show question immediately
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    # Mark question as pending
    st.session_state.pending_question = question

    # Rerun immediately so question becomes visible
    st.rerun()

# ============================
# Generate Answer (Phase 2)
# ============================
if st.session_state.pending_question:
    with st.spinner("🧠 Thinking..."):
        answer = answer_question(
            st.session_state.pending_question,
            chat_history=st.session_state.messages
        )

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    # Clear pending question
    st.session_state.pending_question = None

    st.rerun()
