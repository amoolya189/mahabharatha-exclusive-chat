# preprocess.py
import os

def load_and_chunk_text(folder_path, chunk_size=800):
    texts = []
    filenames = sorted(os.listdir(folder_path))
    for file in filenames:
        file_path = os.path.join(folder_path, file)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().replace("\n", " ").strip()
            # split content into chunks
            for i in range(0, len(content), chunk_size):
                chunk = content[i:i+chunk_size]
                texts.append({"text": chunk, "source": file})
    return texts

if __name__ == "__main__":
    data = load_and_chunk_text("mahabharata_texts")
    print(f"Total chunks: {len(data)}")
