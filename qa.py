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

# ✅ Configure Gemini API (use your key)
genai.configure(api_key="AIzaSyAMsjthTjWOjwpflzHwZbbrV_t6IGHGlcM")

# ======================
# 2️⃣ Helper: Rephrase Queries (for vague or indirect ones)
# ======================
def rephrase_question(question):
    """Ask Gemini to clarify vague or indirect questions."""
    clarifier = genai.GenerativeModel("gemini-2.0-flash")
    prompt = f"""
    You are a helpful assistant. The user asked a question that might be vague or indirect.
    Please rewrite it clearly and directly in a way that helps find relevant information from the Mahabharata.
    
    Original question: {question}
    
    Rephrased (clear) version:
    """
    try:
        response = clarifier.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return question  # fallback


# ======================
# 3️⃣ Main Answer Function
# ======================
def answer_question(question, top_k=5):
    """Find best context and ask Gemini for an accurate answer."""
    
    # Step 1: Rephrase vague queries
    rephrased_q = rephrase_question(question)
    
    # Step 2: Encode and retrieve
    q_emb = model.encode([rephrased_q])
    D, idxs = index.search(np.array(q_emb), top_k)
    context = "\n\n".join([chunks[i]['text'] for i in idxs[0]])
    
    # Step 3: Build a strong reasoning prompt
    prompt = f"""
    You are a knowledgeable Mahabharata scholar. 
    Use the context provided to answer the user's question accurately, logically, and with interpretation when needed.
    If the text doesn't mention something directly, infer based on themes, symbolism, or known interpretations of the Mahabharata.

    Context excerpts:
    {context}

    Original Question: {question}
    Clarified Question: {rephrased_q}

    Provide a detailed, human-like answer:
    """

    gemini_model = genai.GenerativeModel("gemini-2.5-flash")
    
    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Error generating response: {e}"


# ======================
# 4️⃣ CLI Interface
# ======================
if __name__ == "__main__":
    print("🕉️  Mahabharata Q&A System (Enhanced Gemini Mode)")
    print("Type your question below (or 'exit' to quit):\n")

    while True:
        q = input("❓ Your question: ").strip()
        if q.lower() == "exit":
            break
        try:
            print("\n🧠 Thinking...\n")
            print("📜 Answer:\n", answer_question(q), "\n")
        except Exception as e:
            print("⚠️ Error:", e, "\n")
