import { useQuery } from '@tanstack/react-query'
import { getPapers } from '../services/api'

function PaperList() {
  const { data: papers, isLoading, error } = useQuery({
    queryKey: ['papers'],
    queryFn: getPapers,
  })

  if (isLoading) {
    return (
      <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>
        Loading papers...
      </div>
    )
  }

  if (error) {
    return (
      <div style={{ padding: '2rem', textAlign: 'center', color: '#ef4444' }}>
        Error loading papers
      </div>
    )
  }

  if (!papers || papers.length === 0) {
    return (
      <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>
        <p>No papers uploaded yet</p>
        <p style={{ fontSize: '0.875rem', marginTop: '0.5rem' }}>Upload your first paper to get started</p>
      </div>
    )
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
      {papers.map((paper: any) => (
        <div
          key={paper.id}
          style={{
            padding: '1rem',
            border: '1px solid var(--border-color)',
            borderRadius: '8px',
            background: 'var(--bg-primary)',
            transition: 'all 0.2s',
            cursor: 'pointer'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.borderColor = 'var(--primary-purple)'
            e.currentTarget.style.boxShadow = '0 2px 8px rgba(99, 102, 241, 0.1)'
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.borderColor = 'var(--border-color)'
            e.currentTarget.style.boxShadow = 'none'
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.5rem' }}>
            <h3 style={{ fontSize: '1rem', fontWeight: 600, color: 'var(--text-primary)' }}>
              {paper.title}
            </h3>
            <span
              style={{
                padding: '0.25rem 0.5rem',
                borderRadius: '4px',
                fontSize: '0.75rem',
                fontWeight: 500,
                background: paper.processed ? '#d1fae5' : '#fef3c7',
                color: paper.processed ? '#065f46' : '#92400e'
              }}
            >
              {paper.processed ? 'Processed' : 'Pending'}
            </span>
          </div>
          {paper.authors && (
            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>
              {paper.authors}
            </p>
          )}
          <p style={{ fontSize: '0.8125rem', color: 'var(--text-muted)' }}>
            Uploaded {new Date(paper.upload_date).toLocaleDateString()}
          </p>
        </div>
      ))}
    </div>
  )
}

export default PaperList

