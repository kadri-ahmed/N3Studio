interface HomePageProps {
  onNavigate?: (tab: string) => void
}

function HomePage({ onNavigate }: HomePageProps) {
  return (
    <div>
      {/* Hero Section */}
      <div className="hero-section">
        <h1 className="hero-headline">
          Transform Research Papers into<br />
          <span className="hero-highlight">Actionable Knowledge</span>
        </h1>
        <p className="hero-subheadline">
          SummarIQ uses cutting-edge AI, knowledge graphs, and RAG technology to help researchers 
          instantly summarize, explore, and navigate complex scientific literature. Discover hidden 
          connections between papers, extract key insights, and visualize research relationships 
          like never before—all in one intuitive platform.
        </p>
        <div className="hero-cta">
          <button 
            className="btn btn-primary btn-large"
            onClick={() => {
              if (onNavigate) {
                onNavigate('papers')
              }
            }}
          >
            Get Started Free
          </button>
          <button 
            className="btn btn-secondary btn-large"
            onClick={() => {
              if (onNavigate) {
                onNavigate('graph')
              }
            }}
          >
            Explore Knowledge Graph
          </button>
        </div>
        <div className="hero-stats">
          <div className="stat-item">
            <div className="stat-number">Instant</div>
            <div className="stat-label">Summarization</div>
          </div>
          <div className="stat-item">
            <div className="stat-number">Visual</div>
            <div className="stat-label">Knowledge Graphs</div>
          </div>
          <div className="stat-item">
            <div className="stat-number">AI-Powered</div>
            <div className="stat-label">RAG Queries</div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default HomePage

