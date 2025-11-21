import { useState } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { uploadPaper } from '../services/api'

function PaperUpload() {
  const [file, setFile] = useState<File | null>(null)
  const queryClient = useQueryClient()

  const uploadMutation = useMutation({
    mutationFn: uploadPaper,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['papers'] })
      setFile(null)
      alert('Paper uploaded successfully!')
    },
    onError: (error) => {
      alert(`Upload failed: ${error.message}`)
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (file) {
      uploadMutation.mutate(file)
    }
  }

  return (
    <div className="paper-upload">
      <h2>Upload Research Paper</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          disabled={uploadMutation.isPending}
        />
        <button type="submit" disabled={!file || uploadMutation.isPending}>
          {uploadMutation.isPending ? 'Uploading...' : 'Upload Paper'}
        </button>
      </form>
    </div>
  )
}

export default PaperUpload

