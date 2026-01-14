import { useState } from "react";
import { uploadPDF, askQuestion } from "./api";

function App() {
  // stores the PDF file object selected by the user 
  const [file, setFile] = useState(null);
  // stores the document ID returned by backend 
  const [docId, setDocId] = useState(null);
  // stores what the user types in the textArea
  const [question, setQuestion] = useState("");
  // stores the answer returned 
  const [answer, setAnswer] = useState("");
  // tracks whether backend is processing used to show thinking 
  const [loading, setLoading] = useState(false);

  // triggered when user clicks upload pdf
  const handleUpload = async () => {
    if (!file) {
      alert("Please select a PDF");
      return;
    }

    setLoading(true);
    // call api.js -> backend , backend ingests pdf -> build Faiss
    const res = await uploadPDF(file);
    // stores document identity 
    setDocId(res.doc_id);
    setLoading(false);
  };

  // triggers when user clicks Ask
  const handleAsk = async () => {
    if (!question || !docId) return;

    setLoading(true);
    const res = await askQuestion(question, docId);
    setAnswer(res.answer);
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: "700px", margin: "40px auto", fontFamily: "Arial" }}>
      <h2> Chat with PDF (RAG)</h2>

      {/* Upload */}
      <div>
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <button onClick={handleUpload}>Upload PDF</button>
      </div>

       {/* conditional rendering shows only after upload get successful  */}
      {docId && (
        <p style={{ color: "green" }}>
           PDF uploaded successfully
        </p>
      )}

      <hr />

      {/* Ask */}
      <textarea
        rows="3"
        placeholder="Ask a question about the PDF..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        style={{ width: "100%" }}
      />

      <button onClick={handleAsk} disabled={!docId}>
        Ask
      </button>

      {loading && <p> Thinking...</p>}

      {answer && (
        <div style={{ marginTop: "20px" }}>
          <h4>Answer:</h4>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
}

export default App;
