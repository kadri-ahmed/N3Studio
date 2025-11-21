function RightSidebar() {
  const releaseNotes = [
    { date: '2025-11-20', title: 'Knowledge Graph Visualization' },
    { date: '2025-11-19', title: 'RAG Query Interface' },
    { date: '2025-11-18', title: 'Paper Upload & Processing' },
    { date: '2025-11-17', title: 'FalkorDB Integration' },
    { date: '2025-11-16', title: 'GROQ LLM Support' },
    { date: '2025-11-15', title: 'Initial Release' },
  ]

  return (
    <div className="right-sidebar">
      <div className="sidebar-section">
        <div className="sidebar-section-title">Release Notes</div>
        {releaseNotes.map((note, idx) => (
          <div key={idx} className="release-note">
            <div className="release-date">{note.date}</div>
            <div className="release-title">{note.title}</div>
          </div>
        ))}
      </div>

      <div className="sidebar-section">
        <div className="sidebar-section-title">API References</div>
        <a href="#" className="sidebar-footer-link" style={{ display: 'block', padding: '0.5rem 0' }}>
          API Documentation
        </a>
        <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.5rem' }}>
          v1.0.0
        </div>
      </div>
    </div>
  )
}

export default RightSidebar

