import os
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GRPC_TRACE'] = ''

import pickle
import faiss
import numpy as np
import google.generativeai as genai
from sentence_transformers import SentenceTransformer

# ======================
# 1️⃣ Load Models & Data
# ======================

model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index("mahabharata.index")

with open("chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

# ✅ Configure Gemini API
genai.configure(api_key="AIzaSyAMsjthTjWOjwpflzHwZbbrV_t6IGHGlcM")

# ======================
# 2️⃣ Helper: Rephrase Queries
# ======================
def rephrase_question(question):
    """Ask Gemini to clarify vague or indirect questions."""
    clarifier = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""
You are a helpful assistant.
Rewrite the user's question clearly and directly so that
relevant information from the Mahabharata can be retrieved.

Original question:
{question}

Rephrased clear version:
"""

    try:
        response = clarifier.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return question  # fallback


# ======================
# 3️⃣ Main Answer Function (CONTEXT-AWARE)
# ======================
def answer_question(question, chat_history=None, top_k=5):
    """
    question: current user question
    chat_history: list of previous messages (from Streamlit session_state)
    """

    # ----------------------
    # A️⃣ Build conversation context
    # ----------------------
    conversation_context = ""

    if chat_history:
        # Use only last 4 messages (2 Q&A pairs)
        recent_msgs = chat_history[-4:]

        for msg in recent_msgs:
            role = msg["role"].upper()
            content = msg["content"]
            conversation_context += f"{role}: {content}\n"

    # ----------------------
    # B️⃣ Rephrase with context
    # ----------------------
    rephrase_prompt = f"""
The user is asking a question in an ongoing conversation about the Mahabharata.

Conversation so far:
{conversation_context}

Current question:
{question}

Rewrite the current question clearly and explicitly,
resolving pronouns like he/she/they/that event if needed.
"""

    try:
        clarifier = genai.GenerativeModel("gemini-2.0-flash")
        rephrased_q = clarifier.generate_content(rephrase_prompt).text.strip()
    except Exception:
        rephrased_q = question

    # ----------------------
    # C️⃣ Retrieve relevant chunks
    # ----------------------
    q_emb = model.encode([rephrased_q])
    D, idxs = index.search(np.array(q_emb), top_k)

    context = "\n\n".join([chunks[i]['text'] for i in idxs[0]])

    # ----------------------
    # D️⃣ Final Answer Prompt
    # ----------------------
    prompt = f"""
You are a knowledgeable Mahabharata scholar.

Conversation context:
{conversation_context}

Relevant excerpts from the Mahabharata:
{context}

User's clarified question:
{rephrased_q}

Answer the question accurately, logically, and in detail.
If the answer is not stated directly, infer using Mahabharata traditions,
themes, and scholarly interpretations.
"""

    gemini_model = genai.GenerativeModel("gemini-2.5-flash")

    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Error generating response: {e}"


# ======================
# 4️⃣ CLI Interface (still works)
# ======================
if __name__ == "__main__":
    print("🕉️  Mahabharata Q&A System (Context-Aware Gemini Mode)")
    print("Type your question below (or 'exit' to quit):\n")

    history = []

    while True:
        q = input("❓ Your question: ").strip()
        if q.lower() == "exit":
            break

        print("\n🧠 Thinking...\n")
        ans = answer_question(q, chat_history=history)

        print("📜 Answer:\n", ans, "\n")

        history.append({"role": "user", "content": q})
        history.append({"role": "assistant", "content": ans})
