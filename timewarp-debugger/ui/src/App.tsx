import { useState, useEffect, useRef } from 'react'
import './index.css'

interface Event {
  id?: number;
  time: number;
  thread_id?: number;
  event: string;
  function: string;
  line: number;
  source: string;
  depth: number;
  locals: Record<string, any>;
}

function App() {
  const [events, setEvents] = useState<Event[]>([])
  const [currentIndex, setCurrentIndex] = useState<number>(0)
  const [error, setError] = useState<string | null>(null)
  
  // Playground state
  const [code, setCode] = useState<string>("def calculate(a, b):\n    return a + b\n\nprint(calculate(10, 5))")
  const [isRunning, setIsRunning] = useState(false)

  const activeEventRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    fetch('http://localhost:8000/api/events')
      .then(res => res.json())
      .then(data => {
        if (data.error) {
          setError(data.error)
        } else {
          setEvents(data)
          setCurrentIndex(0)
          setError(null)
        }
      })
      .catch(err => setError(err.message))
  }, [])

  useEffect(() => {
    if (activeEventRef.current) {
      activeEventRef.current.scrollIntoView({ behavior: 'smooth', block: 'nearest' })
    }
  }, [currentIndex])

  const handleRunCode = async () => {
    setIsRunning(true)
    setError(null)
    try {
      const res = await fetch('http://localhost:8000/api/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code })
      })
      const data = await res.json()
      if (data.error) {
        setError(data.error)
      } else {
        setEvents(data)
        setCurrentIndex(0)
      }
    } catch (err: any) {
      setError(err.message)
    } finally {
      setIsRunning(false)
    }
  }

  const currentEvent = events[currentIndex]

  return (
    <div className="dashboard">
      <div className="playground-sidebar">
        <div style={{ padding: '16px', borderBottom: '1px solid var(--border-color)', background: 'var(--bg-dark)' }}>
          <h2 style={{ margin: 0, fontSize: '1.1rem', color: 'var(--text-main)' }}>Live Editor</h2>
        </div>
        <textarea 
          className="code-editor"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          spellCheck={false}
        />
        <div style={{ padding: '16px', background: 'var(--bg-dark)' }}>
          <button 
            className="run-btn" 
            onClick={handleRunCode} 
            disabled={isRunning}
            style={{ width: '100%', padding: '12px', fontSize: '1rem' }}
          >
            {isRunning ? 'Running...' : '▶ Run Code & Trace'}
          </button>
        </div>
      </div>

      <div className="sidebar" style={{ width: '280px' }}>
        <div style={{ padding: '16px', borderBottom: '1px solid var(--border-color)', background: 'var(--bg-dark)', position: 'sticky', top: 0, zIndex: 10 }}>
          <h2 style={{ margin: 0, fontSize: '1.1rem', color: 'var(--text-main)' }}>Execution Timeline</h2>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '4px' }}>{events.length} Events</div>
        </div>
        {events.map((ev, idx) => (
          <div 
            key={idx} 
            ref={idx === currentIndex ? activeEventRef : null}
            className={`event-item ${idx === currentIndex ? 'active' : ''}`}
            onClick={() => setCurrentIndex(idx)}
          >
            <div className="event-func">{ev.function}:{ev.line}</div>
            <div className="event-meta">
              [{ev.event}] | Time: {(ev.time || 0).toFixed(4)}s
            </div>
          </div>
        ))}
      </div>

      <div className="main-panel">
        <div className="top-bar">
          <div className="title">
            TimeWarp Debugger Dashboard 
            {events.length > 0 && <span style={{ marginLeft: '12px', fontSize: '0.9rem', color: 'var(--text-muted)', fontWeight: 'normal' }}>
              (Step {currentIndex + 1} / {events.length})
            </span>}
          </div>
          {events.length > 0 && (
            <div className="timeline-controls">
              <button onClick={() => setCurrentIndex(0)} disabled={currentIndex === 0}>First</button>
              <button onClick={() => setCurrentIndex(c => Math.max(0, c - 1))} disabled={currentIndex === 0}>Step Back</button>
              <button onClick={() => setCurrentIndex(c => Math.min(events.length - 1, c + 1))} disabled={currentIndex === events.length - 1}>Step Forward</button>
              <button onClick={() => setCurrentIndex(events.length - 1)} disabled={currentIndex === events.length - 1}>Last</button>
            </div>
          )}
        </div>

        <div className="content-area">
          {error && (
            <div className="panel" style={{ border: '1px solid #ef4444' }}>
              <h2 style={{ color: '#ef4444' }}>Execution Error</h2>
              <pre style={{ color: '#fca5a5', whiteSpace: 'pre-wrap' }}>{error}</pre>
            </div>
          )}

          {!currentEvent ? (
            <div className="empty-state">No execution data. Write code and hit Run.</div>
          ) : (
            <>
              <div className="panel">
                <h2>Source Context</h2>
                <div className="code-block">
                  {currentEvent.source ? currentEvent.source : <i>(No source code available for this frame)</i>}
                </div>
                <div style={{ marginTop: '16px', fontSize: '0.9rem', color: 'var(--text-muted)', display: 'flex', gap: '16px' }}>
                  <span><b>Stack Depth:</b> {currentEvent.depth}</span>
                  <span><b>Thread ID:</b> {currentEvent.thread_id}</span>
                  <span><b>Module:</b> {currentEvent.function}</span>
                </div>
              </div>

              <div className="panel" style={{ flex: 1 }}>
                <h2>Memory Snapshot (Locals)</h2>
                {Object.keys(currentEvent.locals || {}).length === 0 ? (
                  <div style={{ color: 'var(--text-muted)' }}>No local variables detected in this frame.</div>
                ) : (
                  <div className="variables-grid">
                    {Object.entries(currentEvent.locals).map(([key, value]) => (
                      <div key={key} className="var-card">
                        <div className="var-name">{key}</div>
                        <div className="var-value">
                          {typeof value === 'object' ? JSON.stringify(value, null, 2) : String(value)}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
