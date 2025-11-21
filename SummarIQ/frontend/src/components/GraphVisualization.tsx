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
    if (!containerRef.current || !graphData) return

    if (cyRef.current) {
      cyRef.current.destroy()
    }

    cyRef.current = cytoscape({
      container: containerRef.current,
      elements: graphData,
      style: [
        {
          selector: 'node',
          style: {
            'background-color': '#667eea',
            'label': 'data(label)',
            'width': 30,
            'height': 30,
          },
        },
        {
          selector: 'edge',
          style: {
            'width': 2,
            'line-color': '#ccc',
            'target-arrow-color': '#ccc',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
          },
        },
      ],
      layout: {
        name: 'dagre',
        rankDir: 'TB',
      },
    })

    return () => {
      if (cyRef.current) {
        cyRef.current.destroy()
      }
    }
  }, [graphData])

  if (isLoading) return <div>Loading graph...</div>

  return (
    <div className="graph-visualization">
      <h2>Knowledge Graph</h2>
      <div ref={containerRef} style={{ width: '100%', height: '600px', border: '1px solid #333' }} />
    </div>
  )
}

export default GraphVisualization

