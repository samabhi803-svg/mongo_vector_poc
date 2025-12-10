import { useState, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

function App() {
  const [messages, setMessages] = useState([
    { role: 'agent', content: 'Hello! I am your Vector RAG Agent. Ask me anything about your knowledge base.' }
  ])
  const [input, setInput] = useState('')
  const [ingestText, setIngestText] = useState('')
  const [loading, setLoading] = useState(false)

  // Load history on mount
  useEffect(() => {
    fetch('/api/history')
      .then(res => res.json())
      .then(data => {
        if (data && data.length > 0) {
          setMessages(data)
        }
      })
      .catch(err => console.error("Failed to load history", err))
  }, [])

  const sendMessage = async () => {
    if (!input.trim()) return

    const userMsg = { role: 'user', content: input }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    setLoading(true)

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userMsg.content,
          history: messages // Pass current state as history
        })
      })
      const data = await response.json()
      // We don't save to DB here (backend does it), but we update local state
      setMessages(prev => [...prev, { role: 'agent', content: data.response }])
    } catch (error) {
      setMessages(prev => [...prev, { role: 'agent', content: 'Error connecting to server.' }])
    }
    setLoading(false)
  }

  const clearHistory = async () => {
    try {
      await fetch('/api/history', { method: 'DELETE' })
      setMessages([])
    } catch (error) {
      alert("Failed to clear history")
    }
  }

  const handleIngest = async () => {
    if (ingestText.trim()) {
      // Text Ingestion
      try {
        await fetch('/api/ingest', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify([{ content: ingestText }])
        })
        alert('Text ingested successfully!')
        setIngestText('')
      } catch (error) {
        alert('Error ingesting text.')
      }
    }
  }

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('/api/upload', {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      alert(data.message);
    } catch (error) {
      console.error(error);
      alert('Error uploading file.');
    }
    // Reset input
    e.target.value = null;
  }

  return (
    <div className="app-container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>RAG Agent</h1>
        <button onClick={clearHistory} style={{ backgroundColor: '#dc3545', padding: '5px 10px' }}>Clear Chat</button>
      </div>

      {/* Ingest Section */}
      <div className="ingest-section">
        <h3>Add to Knowledge Base</h3>
        <div style={{ display: 'flex', gap: '10px', flexDirection: 'column' }}>
          {/* Text Input */}
          <div style={{ display: 'flex', gap: '10px' }}>
            <input
              value={ingestText}
              onChange={e => setIngestText(e.target.value)}
              placeholder="Type a fact to remember..."
              style={{ flex: 1 }}
            />
            <button onClick={handleIngest}>Ingest Text</button>
          </div>

          {/* File Upload */}
          <div style={{ display: 'flex', gap: '10px', alignItems: 'center', marginTop: '10px' }}>
            <span style={{ color: '#aaa' }}>Or upload a file (PDF/Text):</span>
            <input
              type="file"
              accept=".txt,.pdf,.jpg,.jpeg,.png,.webp"
              onChange={handleFileUpload}
              style={{ border: 'none' }}
            />
          </div>
        </div>
      </div>

      {/* Chat Section */}
      <div className="chat-container">
        <div className="messages">
          {messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.role}`}>
              <strong>{msg.role === 'agent' ? 'Agent' : 'You'}:</strong>
              <div className="markdown-body">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {msg.content}
                </ReactMarkdown>
              </div>
            </div>
          ))}
          {loading && <div className="message agent">Thinking...</div>}
        </div>
        <div className="input-area">
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && sendMessage()}
            placeholder="Ask a question..."
          />
          <button onClick={sendMessage} disabled={loading}>Send</button>
        </div>
      </div>
    </div>
  )
}

export default App
