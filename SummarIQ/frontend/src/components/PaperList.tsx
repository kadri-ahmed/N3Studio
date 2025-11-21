import { useQuery } from '@tanstack/react-query'
import { getPapers } from '../services/api'

function PaperList() {
  const { data: papers, isLoading, error } = useQuery({
    queryKey: ['papers'],
    queryFn: getPapers,
  })

  if (isLoading) return <div>Loading papers...</div>
  if (error) return <div>Error loading papers</div>

  return (
    <div className="paper-list">
      <h2>Uploaded Papers</h2>
      {papers && papers.length > 0 ? (
        <ul>
          {papers.map((paper) => (
            <li key={paper.id}>
              <h3>{paper.title}</h3>
              <p>Uploaded: {new Date(paper.upload_date).toLocaleDateString()}</p>
              <span className={paper.processed ? 'processed' : 'pending'}>
                {paper.processed ? 'Processed' : 'Pending'}
              </span>
            </li>
          ))}
        </ul>
      ) : (
        <p>No papers uploaded yet</p>
      )}
    </div>
  )
}

export default PaperList

