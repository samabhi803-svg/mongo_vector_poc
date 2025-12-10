import { useState } from 'react'

function App() {
  const [messages, setMessages] = useState([
    { role: 'agent', content: 'Hello! I am your Vector RAG Agent. Ask me anything about your knowledge base.' }
  ])
  const [input, setInput] = useState('')
  const [ingestText, setIngestText] = useState('')
  const [loading, setLoading] = useState(false)

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
        body: JSON.stringify({ message: userMsg.content })
      })
      const data = await response.json()
      setMessages(prev => [...prev, { role: 'agent', content: data.response }])
    } catch (error) {
      setMessages(prev => [...prev, { role: 'agent', content: 'Error connecting to server.' }])
    }
    setLoading(false)
  }

  const handleIngest = async () => {
    if (!ingestText.trim()) return
    try {
      await fetch('/api/ingest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify([{ content: ingestText }])
      })
      alert('Document ingested successfully!')
      setIngestText('')
    } catch (error) {
      alert('Error ingesting document.')
    }
  }

  return (
    <div className="app-container">
      <h1>RAG Agent</h1>

      {/* Ingest Section */}
      <div className="ingest-section">
        <h3>Add to Knowledge Base</h3>
        <div style={{ display: 'flex', gap: '10px' }}>
          <input
            value={ingestText}
            onChange={e => setIngestText(e.target.value)}
            placeholder="Type a fact to remember..."
          />
          <button onClick={handleIngest}>Ingest</button>
        </div>
      </div>

      {/* Chat Section */}
      <div className="chat-container">
        <div className="messages">
          {messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.role}`}>
              <strong>{msg.role === 'agent' ? 'Agent' : 'You'}:</strong> {msg.content}
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
