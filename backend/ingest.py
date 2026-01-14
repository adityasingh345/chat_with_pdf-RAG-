from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def ingest_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""

    # extract text from each page 
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    # Chunking
    def chunk_text(text, chunk_size=800, overlap=200):
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += chunk_size - overlap
        return chunks

    chunks = chunk_text(text)

    #  Embeddings 
    embeddings = model.encode(chunks, convert_to_numpy=True)

    # FAISS
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    return index, chunks
