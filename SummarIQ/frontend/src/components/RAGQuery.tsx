import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { queryPapers } from '../services/api'

function RAGQuery() {
  const [query, setQuery] = useState('')
  const [paperIds, setPaperIds] = useState<number[]>([])

  const queryMutation = useMutation({
    mutationFn: (q: string) => queryPapers(q, paperIds.length > 0 ? paperIds : undefined),
    onError: (error: any) => {
      alert(`Query failed: ${error.message || 'Unknown error'}`)
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (query.trim()) {
      queryMutation.mutate(query)
    }
  }

  return (
    <div>
      <form onSubmit={handleSubmit} style={{ marginBottom: '2rem' }}>
        <div style={{ marginBottom: '1rem' }}>
          <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500, fontSize: '0.875rem' }}>
            Enter your question
          </label>
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g., What are the main findings about machine learning in recent papers?"
            rows={6}
            style={{
              width: '100%',
              padding: '0.75rem',
              border: '1px solid var(--border-color)',
              borderRadius: '8px',
              fontSize: '0.9375rem',
              fontFamily: 'inherit',
              resize: 'vertical',
              transition: 'border-color 0.2s'
            }}
            onFocus={(e) => e.currentTarget.style.borderColor = 'var(--primary-purple)'}
            onBlur={(e) => e.currentTarget.style.borderColor = 'var(--border-color)'}
          />
        </div>
        <button
          type="submit"
          className="btn btn-primary"
          disabled={!query.trim() || queryMutation.isPending}
          style={{ width: '100%' }}
        >
          {queryMutation.isPending ? 'Querying...' : 'Query Papers'}
        </button>
      </form>

      {queryMutation.data && (
        <div style={{
          padding: '1.5rem',
          background: 'var(--bg-secondary)',
          borderRadius: '8px',
          border: '1px solid var(--border-color)'
        }}>
          <h3 style={{ fontSize: '1.125rem', fontWeight: 600, marginBottom: '1rem' }}>Answer</h3>
          <p style={{ lineHeight: 1.7, marginBottom: '1.5rem', color: 'var(--text-primary)' }}>
            {queryMutation.data.answer}
          </p>
          
          {queryMutation.data.sources && queryMutation.data.sources.length > 0 && (
            <>
              <h4 style={{ fontSize: '0.9375rem', fontWeight: 600, marginBottom: '0.75rem', color: 'var(--text-primary)' }}>
                Sources
              </h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                {queryMutation.data.sources.map((source: any, idx: number) => (
                  <div
                    key={idx}
                    style={{
                      padding: '0.75rem',
                      background: 'var(--bg-primary)',
                      borderRadius: '6px',
                      border: '1px solid var(--border-color)',
                      fontSize: '0.875rem'
                    }}
                  >
                    {source.title || source.content || `Source ${idx + 1}`}
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      )}
    </div>
  )
}

export default RAGQuery

