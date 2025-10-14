import { useEffect, useMemo, useRef, useState } from 'react'
import './App.css'
import { postChat, postReset } from './api/client'

function generateUuid() {
  // RFC4122 version-4 compliant UUID (simple implementation)
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = (Math.random() * 16) | 0
    const v = c === 'x' ? r : (r & 0x3) | 0x8
    return v.toString(16)
  })
}

function usePersistentSessionId() {
  const [sessionId, setSessionId] = useState(() => {
    const existing = localStorage.getItem('session_id')
    if (existing) return existing
    const fresh = generateUuid()
    localStorage.setItem('session_id', fresh)
    return fresh
  })
  const update = (next) => {
    localStorage.setItem('session_id', next)
    setSessionId(next)
  }
  const renew = () => update(generateUuid())
  return { sessionId, setSessionId: update, renew }
}

function QuickPrompts({ onChoose }) {
  const prompts = [
    'How do I reset my password?',
    'What are your business hours?',
    'What is your refund policy?',
    'I want to talk to a human agent.',
  ]
  return (
    <div className="prompt-grid">
      {prompts.map((p) => (
        <button className="pill" key={p} onClick={() => onChoose(p)}>{p}</button>
      ))}
    </div>
  )
}

function ChatMessage({ user, assistant }) {
  return (
    <div className="chat-message">
      <div className="bubble you"><span className="label">You</span>{user}</div>
      <div className="bubble bot"><span className="label">Assistant</span><div className="bot-text">{assistant}</div></div>
    </div>
  )
}

function App() {
  const { sessionId, renew } = usePersistentSessionId()
  const [chat, setChat] = useState([]) // {user, assistant}
  const [input, setInput] = useState('')
  const [isSending, setIsSending] = useState(false)
  const listRef = useRef(null)

  useEffect(() => {
    if (!listRef.current) return
    listRef.current.scrollTop = listRef.current.scrollHeight
  }, [chat])

  async function handleSend(e) {
    e?.preventDefault?.()
    const text = input.trim()
    if (!text || isSending) return
    setIsSending(true)
    const optimistic = [...chat, { user: text, assistant: '...' }]
    setChat(optimistic)
    setInput('')
    try {
      const res = await postChat({ sessionId, message: text })
      const reply = res?.reply || '(empty response)'
      setChat((prev) => {
        const copy = [...prev]
        copy[copy.length - 1] = { user: text, assistant: reply }
        return copy
      })
    } catch (err) {
      setChat((prev) => {
        const copy = [...prev]
        copy[copy.length - 1] = { user: text, assistant: `❌ ${err.message}` }
        return copy
      })
    } finally {
      setIsSending(false)
    }
  }

  function handleQuickPrompt(p) {
    setInput(p)
  }

  function handleNewSession() {
    renew()
    setChat([])
  }

  async function handleResetBackend() {
    try {
      await postReset({ sessionId })
      setChat((prev) => [...prev, { user: '(system)', assistant: '✅ Session history cleared.' }])
    } catch (e) {
      setChat((prev) => [...prev, { user: '(system)', assistant: `❌ ${e.message}` }])
    }
  }

  return (
    <div className="app">
      <header className="header">
        <div className="brand">AI Customer Support</div>
        <div className="header-actions">
          <button className="secondary" type="button" onClick={handleNewSession}>New chat</button>
          <button className="secondary" type="button" onClick={handleResetBackend}>Reset history</button>
        </div>
      </header>
      <main className="main">
        <section className="chat">
          <div ref={listRef} className="chat-scroll">
            {chat.length === 0 && (
              <div className="empty">Welcome to Unthinkable Solutions AI Customer Support! How can I help you today?</div>
            )}
            {chat.map((m, idx) => (
              <ChatMessage key={idx} user={m.user} assistant={m.assistant} />
            ))}
          </div>
          <form onSubmit={handleSend} className="composer">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              rows={2}
            />
            <button className="primary" type="submit" disabled={isSending || !input.trim()}>Send</button>
            <button className="secondary" type="button" onClick={() => setChat([])}>Clear</button>
          </form>
        </section>
        <aside className="sidebar">
          <div className="section-title">Quick prompts</div>
          <QuickPrompts onChoose={handleQuickPrompt} />
        </aside>
      </main>
    </div>
  )
}

export default App
