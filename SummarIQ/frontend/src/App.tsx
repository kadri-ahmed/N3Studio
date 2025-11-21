import { useState } from 'react'
import Sidebar from './components/Sidebar'
import HomePage from './components/HomePage'
import PaperUpload from './components/PaperUpload'
import PaperList from './components/PaperList'
import GraphVisualization from './components/GraphVisualization'
import RAGQuery from './components/RAGQuery'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState<string>('home')

  const renderContent = () => {
    switch (activeTab) {
      case 'home':
        return <HomePage onNavigate={setActiveTab} />
      case 'papers':
        return (
          <div className="content-page">
            <div className="content-header">
              <h1 className="content-title">Papers</h1>
              <p className="content-subtitle">Manage and explore your research paper collection</p>
            </div>
            <div className="page-section">
              <PaperUpload />
            </div>
            <div className="page-section">
              <PaperList />
            </div>
          </div>
        )
      case 'graph':
        return (
          <div className="content-page">
            <div className="content-header">
              <h1 className="content-title">Knowledge Graph</h1>
              <p className="content-subtitle">Visualize relationships between papers, concepts, and findings</p>
            </div>
            <GraphVisualization />
          </div>
        )
      case 'query':
        return (
          <div className="content-page">
            <div className="content-header">
              <h1 className="content-title">RAG Query</h1>
              <p className="content-subtitle">Ask questions about your paper collection using RAG</p>
            </div>
            <RAGQuery />
          </div>
        )
      default:
        return <HomePage />
    }
  }

  return (
    <div className="app">
      <Sidebar activeTab={activeTab} onTabChange={setActiveTab} />
      <div className="main-content">
        {renderContent()}
      </div>
    </div>
  )
}

export default App

