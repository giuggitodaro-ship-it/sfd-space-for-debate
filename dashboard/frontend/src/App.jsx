import { useState, useEffect, useRef } from 'react'

const AGENT_CONFIG = {
  Cosmo:    { icon: '🔭', color: '#5B8DD9', domain: 'Fisica & Spazio' },
  Hermes:   { icon: '📊', color: '#F5A623', domain: 'Economia' },
  Psiche:   { icon: '🧠', color: '#9B59B6', domain: 'Psicologia' },
  Asclepio: { icon: '⚕️', color: '#2ECC71', domain: 'Medicina' },
  Prometeo: { icon: '🌿', color: '#27AE60', domain: 'Natura & Ecologia' },
  Ares:     { icon: '⚔️', color: '#E74C3C', domain: 'Strategia' },
  Temide:   { icon: '⚖️', color: '#F39C12', domain: 'Diritto' },
}

const LOADING_MSGS = [
  { label: 'Fase 1', text: 'Le AI esprimono le loro opinioni...' },
  { label: 'Fase 2', text: 'Comunicazione telepatica in corso...' },
  { label: 'Fase 3', text: 'Consenso emergente...' },
]

// Estimated timings from real runs (ms)
const PHASE_TIMINGS = [0, 145_000, 315_000]

function AgentCard({ name, phase1, phase2, index }) {
  const cfg = AGENT_CONFIG[name] ?? { icon: '🤖', color: '#888', domain: '' }
  return (
    <div
      className="agent-card"
      style={{ '--accent': cfg.color, animationDelay: `${index * 0.12}s` }}
    >
      <div className="agent-header">
        <span className="agent-icon">{cfg.icon}</span>
        <div>
          <div className="agent-name" style={{ color: cfg.color }}>{name}</div>
          <div className="agent-domain">{cfg.domain}</div>
        </div>
      </div>

      <div className="phase-block">
        <div className="phase-label">Opinione iniziale</div>
        <div className="phase-text">{phase1}</div>
      </div>

      <div className="phase-block phase-block--2">
        <div className="phase-label">Dopo telepatia ↓</div>
        <div className="phase-text">{phase2}</div>
      </div>
    </div>
  )
}

function LoadingState({ phaseIdx }) {
  return (
    <div className="loading-box">
      <div className="loading-phases">
        {LOADING_MSGS.map((m, i) => (
          <div
            key={i}
            className={`lphase ${i < phaseIdx ? 'lphase--done' : ''} ${i === phaseIdx ? 'lphase--active' : ''}`}
          >
            <span className="lphase-dot">
              {i < phaseIdx ? '✓' : i === phaseIdx ? '◆' : '○'}
            </span>
            <span className="lphase-lbl">{m.label}</span>
            <span className="lphase-txt">{m.text}</span>
          </div>
        ))}
      </div>
      <div className="spinner" />
    </div>
  )
}

function ConsensusSection({ result }) {
  const largest = result.gruppi[0] ?? null
  const rest = result.gruppi.slice(1)
  const convergenti = largest?.ai ?? []
  const divergenti = rest.flatMap(g => g.ai)
  const simPct = Math.round(result.avg_similarity_globale * 100)

  return (
    <div className="consensus-box">
      <div className="sec-title">Consenso Emergente</div>

      <div className="vote-row">
        <span className="vote-big">{result.voto}</span>
        <span className="vote-sub">
          {result.unanimita ? 'unanimità' : 'convergenza'}&nbsp;
          <span className="vote-dim">avg sim globale: {result.avg_similarity_globale.toFixed(4)}</span>
        </span>
      </div>

      <div className="sim-bar-wrap">
        <div className="sim-bar">
          <div className="sim-fill" style={{ width: `${simPct}%` }} />
        </div>
      </div>

      <div className="groups-row">
        <div className="group">
          <div className="group-lbl group-lbl--green">Convergenti</div>
          <div className="badges">
            {convergenti.map(n => (
              <span key={n} className="badge badge--green">
                {AGENT_CONFIG[n]?.icon} {n}
              </span>
            ))}
          </div>
        </div>

        {divergenti.length > 0 && (
          <div className="group">
            <div className="group-lbl group-lbl--red">Divergenti</div>
            <div className="badges">
              {divergenti.map(n => (
                <span key={n} className="badge badge--red">
                  {AGENT_CONFIG[n]?.icon} {n}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {largest && (
        <div className="synthesis">
          <div className="synthesis-lbl">Sintesi — agente più centrale</div>
          <div className="synthesis-txt">{largest.sintesi}</div>
        </div>
      )}

      {result.gruppi.length > 1 && (
        <details className="all-groups">
          <summary>Tutti i gruppi ({result.gruppi.length})</summary>
          {result.gruppi.map((g, i) => (
            <div key={i} className="mini-group">
              <span className="mini-group-ai">{g.ai.join(' + ')}</span>
              <span className="mini-group-sim">sim: {g.similarity_media.toFixed(4)}</span>
            </div>
          ))}
        </details>
      )}
    </div>
  )
}

export default function App() {
  const [mi, setMi] = useState('')
  const [loading, setLoading] = useState(false)
  const [phaseIdx, setPhaseIdx] = useState(0)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const timers = useRef([])

  const clearTimers = () => {
    timers.current.forEach(clearTimeout)
    timers.current = []
  }

  useEffect(() => () => clearTimers(), [])

  const submit = async () => {
    if (!mi.trim() || loading) return
    setLoading(true)
    setResult(null)
    setError(null)
    setPhaseIdx(0)

    PHASE_TIMINGS.forEach((delay, i) => {
      timers.current.push(setTimeout(() => setPhaseIdx(i), delay))
    })

    try {
      const res = await fetch('http://localhost:8000/debate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mi: mi.trim() }),
      })
      if (!res.ok) {
        const err = await res.json().catch(() => ({}))
        throw new Error(err.detail ?? `HTTP ${res.status}`)
      }
      setResult(await res.json())
    } catch (e) {
      setError(e.message)
    } finally {
      clearTimers()
      setLoading(false)
    }
  }

  const onKey = e => { if (e.key === 'Enter' && e.ctrlKey) submit() }

  return (
    <div className="app">
      <header className="hdr">
        <div className="logo">SFD</div>
        <div className="tagline">Space for Debate — 7 AI · 1 Consenso</div>
      </header>

      {/* INPUT */}
      <section className="input-sec">
        <textarea
          className="mi-input"
          value={mi}
          onChange={e => setMi(e.target.value)}
          onKeyDown={onKey}
          placeholder="Inietta il tuo M.I."
          disabled={loading}
          rows={3}
        />
        <div className="input-row">
          <button
            className="send-btn"
            onClick={submit}
            disabled={loading || !mi.trim()}
          >
            {loading ? 'ELABORAZIONE...' : 'INVIA'}
          </button>
          <span className="hint">Ctrl + Enter</span>
        </div>
      </section>

      {/* LOADING */}
      {loading && <LoadingState phaseIdx={phaseIdx} />}

      {/* ERROR */}
      {error && <div className="error-box">Errore: {error}</div>}

      {/* RESULTS */}
      {result && (
        <>
          <section className="debate-sec">
            <div className="sec-title">Dibattito</div>
            <div className="mi-echo">M.I.: {result.mi}</div>
            <div className="cards">
              {Object.entries(result.phase1_responses).map(([name, p1], i) => (
                <AgentCard
                  key={name}
                  name={name}
                  phase1={p1}
                  phase2={result.phase2_responses[name] ?? ''}
                  index={i}
                />
              ))}
            </div>
          </section>

          <ConsensusSection result={result} />
        </>
      )}
    </div>
  )
}
