import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { queryPapers } from '../services/api'

function RAGQuery() {
  const [query, setQuery] = useState('')
  const [paperIds, setPaperIds] = useState<number[]>([])

  const queryMutation = useMutation({
    mutationFn: (q: string) => queryPapers(q, paperIds.length > 0 ? paperIds : undefined),
    onError: (error) => {
      alert(`Query failed: ${error.message}`)
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (query.trim()) {
      queryMutation.mutate(query)
    }
  }

  return (
    <div className="rag-query">
      <h2>Query Papers with RAG</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter your question about the papers..."
          rows={4}
          style={{ width: '100%', padding: '0.5rem', marginBottom: '1rem' }}
        />
        <button type="submit" disabled={!query.trim() || queryMutation.isPending}>
          {queryMutation.isPending ? 'Querying...' : 'Query'}
        </button>
      </form>

      {queryMutation.data && (
        <div className="query-result">
          <h3>Answer:</h3>
          <p>{queryMutation.data.answer}</p>
          <h4>Sources:</h4>
          <ul>
            {queryMutation.data.sources.map((source: any, idx: number) => (
              <li key={idx}>{source.title || source.content}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default RAGQuery

