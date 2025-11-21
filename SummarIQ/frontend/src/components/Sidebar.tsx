import { useState } from 'react'

interface SidebarProps {
  activeTab: string
  onTabChange: (tab: string) => void
}

function Sidebar({ activeTab, onTabChange }: SidebarProps) {
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <div className="sidebar-logo">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2L2 7L12 12L22 7L12 2Z" fill="currentColor" fillOpacity="0.8"/>
            <path d="M2 17L12 22L22 17" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            <path d="M2 12L12 17L22 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          SummarIQ
        </div>
      </div>

      <div className="sidebar-org">
        <div style={{ fontWeight: 500, marginBottom: '0.25rem' }}>Default</div>
        <div style={{ color: 'var(--text-muted)', fontSize: '0.8125rem' }}>Ahmed Kadri's Org</div>
      </div>

      <nav className="sidebar-nav">
        <div 
          className={`nav-item ${activeTab === 'home' ? 'active' : ''}`}
          onClick={() => onTabChange('home')}
        >
          <svg className="nav-item-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
          Home
        </div>
        
        <div 
          className={`nav-item ${activeTab === 'papers' ? 'active' : ''}`}
          onClick={() => onTabChange('papers')}
        >
          <svg className="nav-item-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          Papers
        </div>
        
        <div 
          className={`nav-item ${activeTab === 'graph' ? 'active' : ''}`}
          onClick={() => onTabChange('graph')}
        >
          <svg className="nav-item-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
          </svg>
          Knowledge Graph
        </div>
        
        <div 
          className={`nav-item ${activeTab === 'query' ? 'active' : ''}`}
          onClick={() => onTabChange('query')}
        >
          <svg className="nav-item-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          RAG Query
        </div>
      </nav>

      <div className="sidebar-footer">
        <a href="#" className="sidebar-footer-link">Settings</a>
        <a href="#" className="sidebar-footer-link">Integrations</a>
        <a href="#" className="sidebar-footer-link">API Keys</a>
        <a href="#" className="sidebar-footer-link">Documentation</a>
        
        <div className="sidebar-user">
          <div className="user-avatar">AK</div>
          <div className="user-info">
            <div className="user-name">Ahmed Kadri</div>
            <div className="user-plan">Free Plan</div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Sidebar

