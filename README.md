📄 Chat with PDF using RAG (FAISS + Ollama + FastAPI + React)

An end-to-end Retrieval-Augmented Generation (RAG) application that allows users to upload a PDF and ask questions about its content.

The system performs semantic search over the document using FAISS and generates context-grounded answers using a local LLM (Ollama).

⚠️ Built without LangChain to deeply understand how RAG works under the hood.

🚀 Features

📤 Upload any PDF document

✂️ Automatic text extraction & chunking

🧠 Semantic embeddings using Sentence Transformers

🔍 Fast similarity search with FAISS

🤖 Context-aware answers via Ollama (local LLM)

🧩 Backend API built with FastAPI

💻 Simple React frontend for interaction

🔐 Document isolation using doc_id

🏗️ Architecture Overview
User (Browser)
   ↓
React Frontend
   ↓ HTTP
FastAPI Backend
   ↓
PDF → Chunks → Embeddings → FAISS
   ↓
Question → FAISS Search → Context
   ↓
Prompt → Ollama (LLM)
   ↓
Answer → Frontend

🧠 How RAG Works in This Project

PDF Upload

User uploads a PDF from the frontend

Backend extracts text and splits it into overlapping chunks

Embedding & Indexing

Each chunk is converted into a vector embedding

Vectors are stored in a FAISS index (per document)

Document Identification

Each uploaded PDF gets a unique doc_id

FAISS index and chunks are stored under this doc_id

Question Answering

User asks a question with the corresponding doc_id

Backend retrieves top-k relevant chunks

LLM answers using only the retrieved context

🛠️ Tech Stack
Backend

FastAPI – REST API

FAISS – Vector similarity search

Sentence-Transformers – Text embeddings

Ollama – Local LLM inference

PyPDF – PDF text extraction

Frontend

React (Vite) – UI

Fetch API – Backend communication

📁 Project Structure
rag-chat-with-pdf/
│
├── backend/
│   ├── app.py            # FastAPI routes
│   ├── ingest.py         # PDF ingestion logic
│   ├── rag.py            # RAG pipeline
│   ├── requirements.txt
│   └── uploads/
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── api.js
│   │   └── main.jsx
│   └── package.json
│
└── README.md

⚙️ Setup Instructions
1️⃣ Prerequisites

Python 3.9+

Node.js 18+

Ollama installed
👉 https://ollama.com

2️⃣ Start Ollama
ollama pull llama3.1
ollama run llama3.1


(Ollama runs at http://localhost:11434)

3️⃣ Backend Setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload


Backend will run at:

http://127.0.0.1:8000


Swagger UI:

http://127.0.0.1:8000/docs

4️⃣ Frontend Setup
cd frontend
npm install
npm run dev


Frontend runs at:

http://localhost:5173

🧪 How to Use the App

Upload a PDF

Backend returns a doc_id

Ask questions related to that PDF

Receive context-grounded answers

Example questions:

What does the document say about physical wellness?

Summarize the main topics discussed

What are the author’s reading interests?

🔐 Why doc_id?

Each PDF is assigned a unique doc_id to:

Prevent mixing content from different documents

Support multiple uploads

Scope all queries to the correct FAISS index

⚠️ Current Limitations

FAISS indexes are stored in memory

Restarting backend clears uploaded documents

No authentication

One document per doc_id

Ollama makes deployment to free platforms difficult

These are intentional trade-offs for learning clarity.

🚀 Future Improvements

Persist FAISS indexes to disk

Support multiple PDFs per session

Streaming responses to frontend

Add citations (page numbers)

Switchable LLM backend (OpenAI / HF)
