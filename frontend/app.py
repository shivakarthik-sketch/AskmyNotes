from flask import Flask, request, jsonify
from flask_cors import CORS
from PyPDF2 import PdfReader

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Backend is working!"

@app.route("/ask", methods=["POST"])
def ask():

    pdf_file = request.files.get("pdf")
    question = request.form.get("question")

    # Validation
    if not pdf_file:
        return jsonify({
            "error": "No PDF uploaded"
        }), 400

    if not question:
        return jsonify({
            "error": "Question missing"
        }), 400

    # Read PDF
    reader = PdfReader(pdf_file)

    extracted_text = ""

    for page in reader.pages:
        extracted_text += page.extract_text()

    # Simple Answer Logic
    answer = f"""
Question: {question}

PDF Content Preview:
{extracted_text[:1000]}
"""

    return jsonify({
        "answer": answer
    })

if __name__ == "__main__":
    app.run(debug=True)