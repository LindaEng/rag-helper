import { useState } from 'react';
import './App.css';

type Source = {
  content: string;
  source: string;
  similarity_score?: number;
  page_number?: number;
  payload?: {
    page_number: number;
  }
}

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [asking, setAsking] = useState(false);
  const [pageToggle, setPageToggle] = useState(false);
  const [sources, setSources] = useState<Source[]>([]);


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
      setSources(data.sources);
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
        {answer && !pageToggle && (
          <div style={{ marginTop: '20px', background: '#f5f5f5', padding: '15px', borderRadius: '5px' }}>
            <strong>Answer:</strong>
            <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit' }}>{answer}</pre>
            <button onClick={() => setPageToggle(true)}>Show Original Page's ({sources.length} sources)</button>
          </div>
        )}
        {pageToggle && (
          <div style={{ marginTop: '20px', background: '#f5f5f5', padding: '15px', borderRadius: '5px' }}>
            <strong>Original Sources</strong>
              <div style={{ marginTop: '10px', marginBottom: '15px' }}>
                {sources.filter((source) => source.similarity_score > 0.1)
                .map((source, idx) => (
                  <div key={idx} style={{ 
                    border: '1px solid #ddd', 
                    padding: '12px', 
                    marginBottom: '10px', 
                    borderRadius: '5px',
                    background: 'white'
                  }}>
                    <div style={{ fontWeight: 'bold', color: '#007bff', marginBottom: '8px' }}>
                      Page {source.page_number || 'Unknown'}
                      {source.similarity_score && (
                        <span style={{ fontSize: '12px', marginLeft: '10px', color: '#666' }}>
                        (relevance: {(source.similarity_score * 100).toFixed(0)}%)
                        </span>
                      )}
                    </div>
                      <div style={{ fontSize: '14px', lineHeight: '1.5' }}>
                        {source.content.substring(0, 5000)}...
                      </div>                    
                  </div>
                ))
                }
              </div>
            <button onClick={() => setPageToggle(false)}>Show LLM response</button>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;