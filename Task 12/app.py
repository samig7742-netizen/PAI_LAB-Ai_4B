import os
import json
import numpy as np
import faiss
from flask import Flask, render_template, request, jsonify
from sentence_transformers import SentenceTransformer
app = Flask(__name__)
DATA_FILE = 'qna_data.json'
with open(DATA_FILE, 'r') as f:
    qna_data = json.load(f)
questions = [item['question'] for item in qna_data]
answers = [item['answer'] for item in qna_data]
print("Loading Embedding Model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Creating Vector Index...")
question_embeddings = model.encode(questions)
embedding_dim = question_embeddings.shape[1]
index = faiss.IndexFlatL2(embedding_dim)
index.add(np.array(question_embeddings).astype('float32'))
def get_best_response(user_query):
    query_vector = model.encode([user_query]).astype('float32')
    k = 1 
    D, I = index.search(query_vector, k)
    best_index = I[0][0]
    distance = D[0][0]
    if distance < 1.2: 
        return answers[best_index], questions[best_index], float(distance)
    else:
        return "I'm sorry, I couldn't find a precise match in my knowledge base. Can you rephrase?", None, float(distance)
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_input = request.form.get("query")
        if not user_input:
            return render_template("index.html")
        response, matched_q, score = get_best_response(user_input)
        return render_template("index.html", query=user_input, response=response, matched=matched_q, score=score)
    return render_template("index.html")
if __name__ == "__main__":
    os.makedirs('templates', exist_ok=True)
    app.run(debug=True, port=5002)