import os
import re
from typing import List
import pdfplumber
from transformers import AutoTokenizer
from flask import Flask, request, render_template_string


tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/LaBSE")

PDF_DIR = "data"  
PDF_FILE = "HSC26-Bangla1st-Paper.pdf"  
PDF_PATH = os.path.join(PDF_DIR, PDF_FILE)

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>RAG Demo</title>
</head>
<body>
    <h2>📘 Simple Bangla RAG System</h2>
    <form method="post">
        <label for="question">Enter your question (in Bangla or English):</label><br>
        <input type="text" id="question" name="question" style="width: 60%; padding: 10px;" required><br><br>
        <input type="submit" value="Submit" style="padding: 10px 20px;">
    </form>
    {% if result %}
        <h3>🔍 Retrieved Chunk:</h3>
        <p>{{ result }}</p>
    {% endif %}
    {% if expected %}
        <h4>✅ Expected Answer:</h4>
        <p>{{ expected }}</p>
    {% endif %}
</body>
</html>
"""

def extract_text(pdf_path: str) -> str:
    text_pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            raw = page.extract_text() or ""
            clean = re.sub(r"\s+", " ", raw).strip()
            text_pages.append(clean)
    return "\n".join(text_pages)

def chunk_text(text: str, max_tokens: int = 500, overlap: float = 0.5) -> List[str]:
    sentences = re.split(r"(?<=[৷\.])\s+", text)

    chunks: List[str] = []
    current: List[str] = []
    current_len = 0

    for sent in sentences:
        token_ids = tokenizer.encode(sent, add_special_tokens=False)
        sent_len = len(token_ids)

        if current_len + sent_len > max_tokens:
            chunks.append(" ".join(current).strip())
            overlap_count = int(len(current) * overlap)
            carry = current[-overlap_count:] if overlap_count > 0 else []
            current = carry.copy()
            current_len = sum(len(tokenizer.encode(s, add_special_tokens=False)) for s in current)

        current.append(sent)
        current_len += sent_len

    if current:
        chunks.append(" ".join(current).strip())

    return chunks

chunks = chunk_text(extract_text(PDF_PATH))

test_cases = {
    "অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?": "শুম্ভুনাথ",
    "কাকে অনুপমের ভাগ্য দেবতা বলে উল্লেখ করা হয়েছে?": "মামাকে",
    "বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?": "১৫ বছর"
}

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    expected = None
    if request.method == "POST":
        question = request.form["question"]
        best_chunk = max(
            chunks,
            key=lambda chunk: similarity_score(chunk, question)
        )
        result = best_chunk[:1000] + ("..." if len(best_chunk) > 1000 else "")
        expected = test_cases.get(question.strip(), "(no expected answer registered)")
    return render_template_string(HTML_TEMPLATE, result=result, expected=expected)

def similarity_score(text1: str, text2: str) -> float:
    tokens1 = set(text1.lower().split())
    tokens2 = set(text2.lower().split())
    return len(tokens1.intersection(tokens2)) / (len(tokens1.union(tokens2)) + 1e-5)

if __name__ == "__main__":
    app.run(debug=True, port=7860)