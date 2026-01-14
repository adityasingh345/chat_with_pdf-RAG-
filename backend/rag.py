import json
import requests
from sentence_transformers import SentenceTransformer

# calling the same model which was there in ingest.py
model = SentenceTransformer("all-MiniLM-L6-v2")

# calling ollama
def call_llm(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.1",
            "prompt": prompt,
            "stream": True
        },
        stream=True,
        timeout=120
    )

    full_response = ""

    for line in response.iter_lines():
        if not line:
            continue

        #  decode bytes → string
        line = line.decode("utf-8").strip()

        # skip non-json lines
        if not (line.startswith("{") and line.endswith("}")):
            continue

        try:
            data = json.loads(line)
            full_response += data.get("response", "")
        except json.JSONDecodeError:
            continue

    return full_response.strip()


def ask_question(query, index, chunks, k=5):
    q_emb = model.encode([query], convert_to_numpy=True)
    _, indices = index.search(q_emb, k)

    context = "\n\n".join([chunks[i] for i in indices[0]])

    prompt = f"""
You are a helpful assistant.

Answer the question using only the context below.
If the answer is not present, say "I don't know".

Context:
{context}

Question:
{query}

Answer:
"""

    return call_llm(prompt)
