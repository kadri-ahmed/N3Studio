import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Papers API
export const uploadPaper = async (file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  const response = await api.post('/api/v1/papers/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return response.data
}

export const getPapers = async () => {
  const response = await api.get('/api/v1/papers')
  return response.data
}

export const getPaper = async (id: number) => {
  const response = await api.get(`/api/v1/papers/${id}`)
  return response.data
}

export const processPaper = async (id: number) => {
  const response = await api.post(`/api/v1/papers/${id}/process`)
  return response.data
}

// Graph API
export const getGraphNodes = async (label?: string) => {
  const params = label ? { label } : {}
  const response = await api.get('/api/v1/graph/nodes', { params })
  return response.data
}

export const getGraphEdges = async (relationship?: string) => {
  const params = relationship ? { relationship } : {}
  const response = await api.get('/api/v1/graph/edges', { params })
  return response.data
}

export const queryGraph = async (entity: string, depth: number = 2) => {
  const response = await api.get('/api/v1/graph/query', {
    params: { entity, depth },
  })
  return response.data
}

export const getGraphVisualization = async (paperId?: number) => {
  const params = paperId ? { paper_id: paperId } : {}
  const response = await api.get('/api/v1/graph/visualization', { params })
  return response.data
}

// RAG API
export const summarizePaper = async (paperId: number, focusAreas?: string[]) => {
  const response = await api.post('/api/v1/rag/summarize', {
    paper_id: paperId,
    focus_areas: focusAreas,
  })
  return response.data
}

export const queryPapers = async (query: string, paperIds?: number[], topK: number = 5) => {
  const response = await api.post('/api/v1/rag/query', {
    query,
    paper_ids: paperIds,
    top_k: topK,
  })
  return response.data
}

export const recommendPapers = async (
  paperId: number,
  basedOn: string = 'similarity',
  limit: number = 5
) => {
  const response = await api.post('/api/v1/rag/recommend', {
    paper_id: paperId,
    based_on: basedOn,
    limit,
  })
  return response.data
}

