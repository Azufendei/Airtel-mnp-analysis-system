import { useState } from 'react'
import { useAuth } from './AuthContext'
import { apiClient } from './api'
import { MNPAnalysisResponse } from './types'
import SearchForm from './SearchForm'
import JourneyTable from './JourneyTable'
import LogsAnalysis from './LogsAnalysis'
import Suggestions from './Suggestions'
import './Dashboard.css'

export default function Dashboard() {
  const { olmId, logout } = useAuth()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [result, setResult] = useState<MNPAnalysisResponse | null>(null)
  const [activeTab, setActiveTab] = useState('journey')

  const handleSearch = async (msisdn: string, startTime?: string, endTime?: string) => {
    setLoading(true)
    setError('')
    setResult(null)

    try {
      if (!olmId) {
        setError('Authentication lost. Please login again.')
        return
      }

      const response = await apiClient.analyzeMNP({
        msisdn,
        olm_id: olmId,
        start_time: startTime,
        end_time: endTime
      })

      setResult(response)
      setActiveTab('journey')
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to analyze MNP'
      setError(errorMessage)
      console.error('Analysis error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <div className="header-left">
          <h1> MNP Journey Analyzer</h1>
          <p className="subtitle">Mobile Number Portability Analysis & Intelligence</p>
        </div>
        <div className="header-right">
          <span className="user-info">👤 {olmId}</span>
          <button onClick={logout} className="logout-button">Logout</button>
        </div>
      </header>

      <main className="dashboard-content">
        <section className="search-section">
          <SearchForm onSearch={handleSearch} loading={loading} />
        </section>

        {error && (
          <div className="error-banner">
            <span className="error-icon">⚠️</span>
            <span className="error-text">{error}</span>
            <button className="close-error" onClick={() => setError('')}>×</button>
          </div>
        )}

        {result && (
          <section className="results-section">
            <div className="results-header">
              <h2>Analysis Results</h2>
              <div className="time-range">
                <span className="label">MSISDN:</span> <code>{result.msisdn}</code>
                <span className="label" style={{ marginLeft: '20px' }}>Time Range:</span>{' '}
                {new Date(result.time_range.start).toLocaleDateString()} to{' '}
                {new Date(result.time_range.end).toLocaleDateString()}
              </div>
            </div>

            <div className="tabs-container">
              <div className="tabs-header">
                <button
                  className={`tab-button ${activeTab === 'journey' ? 'active' : ''}`}
                  onClick={() => setActiveTab('journey')}
                >
                  📋 MNP Journey ({result.tabular_journey.length})
                </button>
                <button
                  className={`tab-button ${activeTab === 'logs' ? 'active' : ''}`}
                  onClick={() => setActiveTab('logs')}
                >
                  📝 Logs Analysis
                </button>
                <button
                  className={`tab-button ${activeTab === 'suggestions' ? 'active' : ''}`}
                  onClick={() => setActiveTab('suggestions')}
                >
                  💡 Suggestions ({result.suggestions.length})
                </button>
              </div>

              <div className="tabs-content">
                {activeTab === 'journey' && (
                  <div className="tab-pane">
                    <JourneyTable events={result.tabular_journey} />
                    {result.tabular_text && (
                      <div className="raw-text-view">
                        <h4>Formatted Journey</h4>
                        <pre>{result.tabular_text}</pre>
                      </div>
                    )}
                  </div>
                )}

                {activeTab === 'logs' && (
                  <div className="tab-pane">
                    <LogsAnalysis analysis={result.logs_analysis} />
                  </div>
                )}

                {activeTab === 'suggestions' && (
                  <div className="tab-pane">
                    <Suggestions suggestions={result.suggestions} msisdn={result.msisdn} />
                  </div>
                )}
              </div>
            </div>

            <div className="results-actions">
              <button className="action-button print" onClick={() => window.print()}>
                🖨️ Print
              </button>
              <button
                className="action-button export"
                onClick={() => {
                  const dataStr = JSON.stringify(result, null, 2)
                  const dataBlob = new Blob([dataStr], { type: 'application/json' })
                  const url = URL.createObjectURL(dataBlob)
                  const link = document.createElement('a')
                  link.href = url
                  link.download = `mnp-analysis-${result.msisdn}-${Date.now()}.json`
                  link.click()
                }}
              >
                💾 Export JSON
              </button>
            </div>
          </section>
        )}

        {!result && !error && (
          <section className="empty-state">
            <div className="empty-icon">🔍</div>
            <h3>Enter MSISDN to analyze</h3>
            <p>Use the search form above to get started with MNP journey analysis</p>
          </section>
        )}
      </main>

      <footer className="dashboard-footer">
        <p>MNP AI Bot v1.0.0 | Secure Mobile Number Portability Analysis</p>
      </footer>
    </div>
  )
}
