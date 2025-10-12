# 🕉️ Mahabharata GPT

A **Streamlit-based web app** that allows users to ask questions about the Mahabharata and get detailed, scholarly answers. Powered by a custom `qa.py` module and optionally OpenAI GPT models.

---

## Features

- Beautiful full-screen Mahabharata-themed background.
- Bold **Lucida Calligraphy** font for headings and labels.
- Black text boxes with white text for better readability.
- Scrollable answer box with adjustable height.
- Responsive question submission with instant answers.
- Works offline with preprocessed text chunks or online with GPT API.

---

## Project Structure

 ```text
MAHABHARATAQA/
├── __pycache__/             
├── .venv/                   
├── mahabharata_texts/       
│   ├── 01 ADI PARVA.txt
│   ├── 02 SABHA PARVA.txt
│   ├── 03 VANA PARVA.txt
│   ├── 04 VIRATA PARVA.txt
│   ├── 05 UDYOGA PARVA.txt
│   ├── 06 BHISHMA PARVA.txt
│   ├── 07 DRONA PARVA.txt
│   ├── 08 Karna-parva.txt
│   ├── 09 Shalya-parva.txt
│   ├── 10 Sauptika-parva.txt
│   ├── 11 Stri-parva.txt
│   ├── 12 SANTI PARVA.txt
│   ├── 13 ANUSASANA PARVA.txt
│   ├── 14 ASWAMEDHA PARVA.txt
│   ├── 15 ASRAMAVASIKA PARVA.txt
│   ├── 16 Mausala-parva.txt
│   ├── 17 Mahaprasthanika-parva.txt
│   └── 18 Svargarohanika-parva.txt
├── app.py                   
├── build_index.py           
├── chunks.pkl               
├── mahabharata.index        
├── preprocess.py            
├── qa.py                    
├── README.md                
└── requirements.txt         

---

# Screenshots

![Mahabharata GPT Screenshot](assets/s.png)


# Installation

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/MAHABHARATAQA.git
cd MAHABHARATAQA

# Create a virtual environment (recommended):

python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate


# Install dependencies:

pip install -r requirements.txt


# Set up environment variables (if using OpenAI API):

Create a .env file in the root folder:

# GEMINI_API_KEY="your_gemini_api_key_here"

#Usage

Run the Streamlit app:

streamlit run app.py
