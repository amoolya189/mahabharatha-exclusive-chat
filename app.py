# app.py
import streamlit as st
from qa import answer_question

# ============================
# Streamlit page configuration
# ============================
st.set_page_config(page_title="Mahabharata GPT", page_icon="🕉️", layout="centered")

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
    top: 0;
    left: 0;
    height: 100%;
    width: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: -1;
}

/* All text bold black (headings, paragraphs, labels) */
h1, h2, h3, h4, h5, h6, p, label, span, div {
    color: #000000 !important;
    font-weight: bold !important;
    font-family: 'Lucida Calligraphy', serif;
}

/* Text input styling - black background, white text */
.stTextInput>div>input {
    background-color: #000000 !important;
    color: #FFFFFF !important;
    font-weight: bold !important;
    border: 2px solid #FFFFFF !important;
}

/* Textarea styling - black background, white text */
.stTextArea>div>textarea {
    background-color: #000000 !important;
    color: #FFFFFF !important;
    font-weight: bold !important;
    border: 2px solid #FFFFFF !important;
}

/* Button styling */
.stButton>button {
    background-color: #FFD700;
    color: black;
    font-weight: bold;
    width: 100%;
    border: 2px solid #000000;
}

div.stButton>button:hover {
    background-color: #FFC107;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# ============================
# App UI
# ============================
st.title("🕉️ Mahabharata GPT - Ask Anything!")

st.markdown(
    "<p style='text-align: center; color: black; font-size:18px; font-weight:bold;'>Ask any question about the Mahabharata and get a detailed, scholarly answer.</p>",
    unsafe_allow_html=True
)

# Centered input
question = st.text_input("Your Question:")

if st.button("Ask"):
    if question.strip():
        with st.spinner("🧠 Thinking..."):
            answer = answer_question(question)
        # Scrollable answer box
        st.text_area("Answer:", value=answer, height=450)
    else:
        st.warning("Please enter a question.")
