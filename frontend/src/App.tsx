import { useState } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [asking, setAsking] = useState(false);
  const [pages, setPages] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      setMessage('Please select a PDF file');
      return;
    }

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/api/upload', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      setMessage(`✅ ${data.message} - ${data.chunks_stored} chunks stored`);
    } catch (error) {
      setMessage('❌ Upload failed. Make sure the backend is running on port 8000');
    } finally {
      setUploading(false);
    }
  };

  const handleAsk = async () => {
    if (!question.trim()) {
      setAnswer('Please enter a question');
      return;
    }

    setAsking(true);
    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      });

      const data = await response.json();
      console.log("MY DATAAA ", data)
      setAnswer(data.answer);
    } catch (error) {
      setAnswer('❌ Failed to get answer. Make sure the backend is running');
    } finally {
      setAsking(false);
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <h1>📚 RAG PDF Assistant</h1>
      
      <div style={{ border: '2px dashed #ccc', padding: '20px', marginBottom: '20px' }}>
        <h2>1. Upload PDF</h2>
        <input 
          type="file" 
          accept=".pdf" 
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />
        <button onClick={handleUpload} disabled={uploading}>
          {uploading ? 'Uploading...' : 'Upload'}
        </button>
        {message && <p>{message}</p>}
      </div>

      <div style={{ border: '2px solid #ccc', padding: '20px' }}>
        <h2>2. Ask a Question</h2>
        <textarea
          rows={3}
          style={{ width: '100%', padding: '8px' }}
          placeholder="Ask anything about your PDF..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <button onClick={handleAsk} disabled={asking}>
          {asking ? 'Thinking...' : 'Ask'}
        </button>
        {answer && !pages && (
          <div style={{ marginTop: '20px', background: '#f5f5f5', padding: '15px', borderRadius: '5px' }}>
            <strong>Answer:</strong>
            <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit' }}>{answer}</pre>
            <button onClick={() => setPages(true)}>Show Original Page's</button>
          </div>
        )}
        {pages && (
          <div style={{ marginTop: '20px', background: '#f5f5f5', padding: '15px', borderRadius: '5px' }}>
            <p>I GOT CLICKED</p>
            <button onClick={() => setPages(false)}>Show LLM response</button>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;