import { useState } from 'react'
import { LogsAnalysis as LogsAnalysisType } from './types'
import './LogsAnalysis.css'

interface LogsAnalysisProps {
  analysis: LogsAnalysisType
}

export default function LogsAnalysis({ analysis }: LogsAnalysisProps) {
  const [expandedIssue, setExpandedIssue] = useState<number | null>(null)

  return (
    <div className="logs-analysis-container">
      <div className="analysis-header">
        <h3>Logs Analysis Summary</h3>
        <p className="summary-text">{analysis.summary}</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-value">{Object.keys(analysis.timeline).reduce((sum, key) => sum + analysis.timeline[key], 0)}</div>
          <div className="stat-label">Total Logs</div>
        </div>
        <div className="stat-card error">
          <div className="stat-value">{analysis.error_count}</div>
          <div className="stat-label">Errors</div>
        </div>
        <div className="stat-card warning">
          <div className="stat-value">{analysis.warning_count}</div>
          <div className="stat-label">Warnings</div>
        </div>
        <div className="stat-card info">
          <div className="stat-value">{analysis.info_count}</div>
          <div className="stat-label">Info</div>
        </div>
      </div>

      {analysis.key_issues.length > 0 && (
        <div className="issues-section">
          <h4>Key Issues Detected</h4>
          <div className="issues-list">
            {analysis.key_issues.map((issue, idx) => (
              <div key={idx} className="issue-item">
                <button
                  className="issue-header"
                  onClick={() => setExpandedIssue(expandedIssue === idx ? null : idx)}
                >
                  <span className="issue-icon">⚠️</span>
                  <span className="issue-text">{issue}</span>
                  <span className="expand-icon">
                    {expandedIssue === idx ? '▼' : '▶'}
                  </span>
                </button>
                {expandedIssue === idx && (
                  <div className="issue-details">
                    {/* Additional details can be expanded here */}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {Object.keys(analysis.timeline).length > 0 && (
        <div className="timeline-section">
          <h4>Event Timeline</h4>
          <div className="timeline">
            {Object.entries(analysis.timeline).map(([time, count], idx) => {
              const maxCount = Math.max(...Object.values(analysis.timeline), 1)
              const widthPercent = Math.min((count / maxCount) * 100, 100)
              return (
                <div key={idx} className="timeline-item">
                  <span className="timeline-time">{time}</span>
                  <div className="timeline-bar">
                    <div
                      className="timeline-fill"
                      style={{
                        width: `${widthPercent}%`
                      }}
                    />
                  </div>
                  <span className="timeline-count">{count}</span>
                </div>
              )
            })}
          </div>
        </div>
      )}
    </div>
  )
}
