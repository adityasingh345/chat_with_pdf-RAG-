// this is the api.js where frontend talks to backend 

// providing backend URL, where the backend is running 
const BASE_URL = "http://127.0.0.1:8000";

// uploading pdf:- sends the selected PDF file to backend 
export async function uploadPDF(file) {
  // creating FromData  why ? because PDFs are binary files JSON can not send files multipart/form-data is required 
  const formData = new FormData();
  formData.append("file", file);

    // sends request to bacckend 
  const res = await fetch(`${BASE_URL}/upload`, {
    method: "POST",
    body: formData,
  });
  // parse backend response 
  return res.json();
}

// asking questions :- aska a question about a specific uploaded PDF uses RAG pipeline on backend 
export async function askQuestion(question, doc_id) {
  // this tells backend what to ask which document to search
  // send request  
  // backend maps this to class QuestionRequest(BaseModel):
    // question: str
    // doc_id: str

  const res = await fetch(`${BASE_URL}/ask`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      question,
      doc_id,
    }),
  });

  // parse response
  return res.json();
}
