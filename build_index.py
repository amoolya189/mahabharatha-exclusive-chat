# build_index.py
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
from preprocess import load_and_chunk_text

# Load chunks
chunks = load_and_chunk_text("mahabharata_texts")

# Create embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
texts = [c['text'] for c in chunks]
embeddings = model.encode(texts, show_progress_bar=True)

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

# Save index and chunks
faiss.write_index(index, "mahabharata.index")
with open("chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

print("Index and chunks saved!")
