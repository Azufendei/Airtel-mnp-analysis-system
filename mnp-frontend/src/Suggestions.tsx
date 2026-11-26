import { useState } from 'react'
import { Suggestion as SuggestionType } from './types'
import './Suggestions.css'

interface SuggestionsProps {
  suggestions?: SuggestionType[] // optional; normalized to array inside component
  msisdn: string
}

export default function Suggestions({ suggestions, msisdn }: SuggestionsProps) {
  const [expandedIdx, setExpandedIdx] = useState<number | null>(null)

  const getPriorityColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'critical':
        return '#dc2626'
      case 'high':
        return '#ea580c'
      case 'medium':
        return '#f59e0b'
      case 'low':
        return '#10b981'
      default:
        return '#6b7280'
    }
  }

  const getPriorityBadge = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'critical':
        return '🔴'
      case 'high':
        return '🟠'
      case 'medium':
        return '🟡'
      case 'low':
        return '🟢'
      default:
        return '⚪'
    }
  }

  const safeSuggestions = Array.isArray(suggestions) ? suggestions : []
  const groupedSuggestions = safeSuggestions.reduce((acc, sugg) => {
    if (!acc[sugg.category]) {
      acc[sugg.category] = []
    }
    acc[sugg.category].push(sugg)
    return acc
  }, {} as Record<string, SuggestionType[]>)

  return (
    <div className="suggestions-container">
      <div className="suggestions-header">
        <h3>End-to-End Suggestions & Recommendations</h3>
        <p className="msisdn-context">MSISDN: <code>{msisdn}</code></p>
      </div>

      {safeSuggestions.length === 0 ? (
        <div className="no-suggestions">
          <p>✓ No issues detected. The MNP journey appears to be normal.</p>
        </div>
      ) : (
        <div className="suggestions-list">
          {Object.entries(groupedSuggestions).map(([category, items]) => (
            <div key={category} className="category-group">
              <h4 className="category-title">📁 {category}</h4>
              <div className="items-list">
                {items.map((suggestion, idx) => (
                  <div
                    key={idx}
                    className="suggestion-item"
                    style={{
                      borderLeftColor: getPriorityColor(suggestion.priority)
                    }}
                  >
                    <button
                      className="suggestion-header"
                      onClick={() => setExpandedIdx(expandedIdx === idx ? null : idx)}
                    >
                      <span className="priority-badge">
                        {getPriorityBadge(suggestion.priority)}
                      </span>
                      <span className="priority-label">{suggestion.priority}</span>
                      <span className="suggestion-title">{suggestion.suggestion}</span>
                      <span className="expand-icon">
                        {expandedIdx === idx ? '▼' : '▶'}
                      </span>
                    </button>
                    {expandedIdx === idx && (
                      <div className="suggestion-details">
                        <p>{suggestion.details}</p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="suggestions-footer">
        <div className="legend">
          <div className="legend-item">
            <span className="priority-badge">🔴</span> Critical
          </div>
          <div className="legend-item">
            <span className="priority-badge">🟠</span> High
          </div>
          <div className="legend-item">
            <span className="priority-badge">🟡</span> Medium
          </div>
          <div className="legend-item">
            <span className="priority-badge">🟢</span> Low
          </div>
        </div>
      </div>
    </div>
  )
}
