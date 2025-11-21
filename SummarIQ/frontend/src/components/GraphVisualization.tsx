import { useEffect, useRef } from 'react'
import { useQuery } from '@tanstack/react-query'
import { getGraphVisualization } from '../services/api'
import cytoscape from 'cytoscape'
import dagre from 'cytoscape-dagre'

cytoscape.use(dagre)

function GraphVisualization() {
  const containerRef = useRef<HTMLDivElement>(null)
  const cyRef = useRef<cytoscape.Core | null>(null)

  const { data: graphData, isLoading } = useQuery({
    queryKey: ['graph-visualization'],
    queryFn: getGraphVisualization,
  })

  useEffect(() => {
    if (!containerRef.current) return

    if (cyRef.current) {
      cyRef.current.destroy()
    }

    // Initialize with empty graph or actual data
    const elements = graphData?.nodes && graphData.nodes.length > 0 
      ? graphData 
      : { nodes: [], edges: [] }

    cyRef.current = cytoscape({
      container: containerRef.current,
      elements: elements,
      style: [
        {
          selector: 'node',
          style: {
            'background-color': 'var(--primary-purple)',
            'label': 'data(label)',
            'width': 40,
            'height': 40,
            'color': '#fff',
            'font-size': '12px',
            'text-valign': 'center',
            'text-halign': 'center',
            'border-width': 2,
            'border-color': '#fff',
            'shape': 'round-rectangle'
          },
        },
        {
          selector: 'edge',
          style: {
            'width': 2,
            'line-color': 'var(--text-muted)',
            'target-arrow-color': 'var(--text-muted)',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
            'opacity': 0.6
          },
        },
      ],
      layout: {
        name: 'dagre',
        rankDir: 'TB',
        spacingFactor: 1.5,
      },
    })

    return () => {
      if (cyRef.current) {
        cyRef.current.destroy()
      }
    }
  }, [graphData])

  if (isLoading) {
    return (
      <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>
        Loading graph...
      </div>
    )
  }

  return (
    <div>
      <div
        ref={containerRef}
        style={{
          width: '100%',
          height: '600px',
          border: '1px solid var(--border-color)',
          borderRadius: '8px',
          background: 'var(--bg-primary)'
        }}
      />
      {(!graphData || (graphData.nodes && graphData.nodes.length === 0)) && (
        <div style={{
          marginTop: '1rem',
          padding: '1rem',
          background: 'var(--bg-secondary)',
          borderRadius: '8px',
          textAlign: 'center',
          color: 'var(--text-muted)'
        }}>
          <p>No graph data available. Upload and process papers to build the knowledge graph.</p>
        </div>
      )}
    </div>
  )
}

export default GraphVisualization

