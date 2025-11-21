import { useState } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { uploadPaper } from '../services/api'

function PaperUpload() {
  const [file, setFile] = useState<File | null>(null)
  const [dragActive, setDragActive] = useState(false)
  const queryClient = useQueryClient()

  const uploadMutation = useMutation({
    mutationFn: uploadPaper,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['papers'] })
      setFile(null)
      alert('Paper uploaded successfully!')
    },
    onError: (error: any) => {
      alert(`Upload failed: ${error.message || 'Unknown error'}`)
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (file) {
      uploadMutation.mutate(file)
    }
  }

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0]
      if (droppedFile.name.endsWith('.pdf')) {
        setFile(droppedFile)
      }
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <div
        className={`upload-area ${dragActive ? 'drag-active' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ marginBottom: '1rem', color: 'var(--text-muted)' }}>
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
          <polyline points="17 8 12 3 7 8" />
          <line x1="12" y1="3" x2="12" y2="15" />
        </svg>
        <p style={{ marginBottom: '0.5rem', fontWeight: 500 }}>Drop your PDF here or click to browse</p>
        <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', marginBottom: '1rem' }}>
          Supported format: PDF
        </p>
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          disabled={uploadMutation.isPending}
          style={{ display: 'none' }}
          id="file-input"
        />
        <label htmlFor="file-input" className="btn btn-secondary" style={{ cursor: 'pointer', display: 'inline-block' }}>
          Select File
        </label>
        {file && (
          <div style={{ marginTop: '1rem', padding: '0.75rem', background: 'var(--bg-secondary)', borderRadius: '6px' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <span style={{ fontSize: '0.875rem' }}>{file.name}</span>
              <button
                type="button"
                onClick={() => setFile(null)}
                style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}
              >
                ×
              </button>
            </div>
          </div>
        )}
      </div>
      <button
        type="submit"
        className="btn btn-primary"
        disabled={!file || uploadMutation.isPending}
        style={{ marginTop: '1rem', width: '100%' }}
      >
        {uploadMutation.isPending ? 'Uploading...' : 'Upload Paper'}
      </button>
    </form>
  )
}

export default PaperUpload

