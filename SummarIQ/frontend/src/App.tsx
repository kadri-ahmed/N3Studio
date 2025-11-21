import { useState } from 'react'
import PaperUpload from './components/PaperUpload'
import PaperList from './components/PaperList'
import GraphVisualization from './components/GraphVisualization'
import RAGQuery from './components/RAGQuery'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState<'papers' | 'graph' | 'query'>('papers')

  return (
    <div className="app">
      <header className="app-header">
        <h1>SummarIQ</h1>
        <p>Research Paper Summarization and Exploration Tool</p>
      </header>

      <nav className="app-nav">
        <button 
          className={activeTab === 'papers' ? 'active' : ''}
          onClick={() => setActiveTab('papers')}
        >
          Papers
        </button>
        <button 
          className={activeTab === 'graph' ? 'active' : ''}
          onClick={() => setActiveTab('graph')}
        >
          Knowledge Graph
        </button>
        <button 
          className={activeTab === 'query' ? 'active' : ''}
          onClick={() => setActiveTab('query')}
        >
          RAG Query
        </button>
      </nav>

      <main className="app-main">
        {activeTab === 'papers' && (
          <div>
            <PaperUpload />
            <PaperList />
          </div>
        )}
        {activeTab === 'graph' && <GraphVisualization />}
        {activeTab === 'query' && <RAGQuery />}
      </main>
    </div>
  )
}

export default App

