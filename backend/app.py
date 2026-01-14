from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from ingest import ingest_pdf
from rag import ask_question
import os
import uuid

app = FastAPI(title="RAG PDF Chat")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# In-memory store (simple version)
VECTOR_STORE = {}

# defining the QuestionRequest
class QuestionRequest(BaseModel):
    question: str
    doc_id: str


@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):
    # unique doc_id generated 
    doc_id = str(uuid.uuid4())
    # putting the pdf into the desired folder that is uploads 
    file_path = f"{UPLOAD_DIR}/{doc_id}.pdf"

    # reading the pdf/file 
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # calling ingest_pdf function to convert the complete pdf into vector embeddings
    index, chunks = ingest_pdf(file_path)

    # saving the index and chunks of the specific file upload and the index is the doc_id 
    VECTOR_STORE[doc_id] = {
        "index": index,
        "chunks": chunks
    }

    # if the file uploaded successfully then we will display the message that pdf uploaded successfully
    return {
        "message": "PDF uploaded and indexed successfully",
        "doc_id": doc_id
    }

# this is for asking question from the uploaded pdf 
@app.post("/ask")
def ask(req: QuestionRequest):
    #we are getting the doc_id 
    store = VECTOR_STORE.get(req.doc_id)

    # if we dont give the required doc_id it will return invalid message 
    if not store:
        return {"answer": "Invalid document ID"}

    # if we have the correct doc_id we will call ask_question function passing the query that is question, index and chunks
    answer = ask_question(
        req.question,
        store["index"],
        store["chunks"]
    )

    # and we will return answer 
    return {"answer": answer}
