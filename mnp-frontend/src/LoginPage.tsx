import React, { useState } from 'react'
import { useAuth } from './AuthContext.tsx'
import './LoginPage.css'

export default function LoginPage() {
  const [olmId, setOlmId] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { isAuthenticated, login } = useAuth()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      if (!olmId.trim()) {
        setError('Please enter a valid OLM ID')
        setLoading(false)
        return
      }

      // Validate against backend users (optional check)
      // For now, just authenticate the user
      login(olmId)
    } catch (err) {
      setError('Failed to authenticate. Please try again.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  if (isAuthenticated) {
    return null
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h1>MNP Journey Analyzer</h1>
          <p>Mobile Number Portability Analysis & Intelligence</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="olmId">OLM ID</label>
            <input
              id="olmId"
              type="text"
              placeholder="Enter your OLM ID"
              value={olmId}
              onChange={(e) => setOlmId(e.target.value)}
              disabled={loading}
              className="form-input"
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <button
            type="submit"
            disabled={loading || !olmId.trim()}
            className="submit-button"
          >
            {loading ? 'Authenticating...' : 'Login'}
          </button>
        </form>

        <div className="login-footer">
          <p>Enter your OLM ID to access MNP journey analysis</p>
        </div>
      </div>
    </div>
  )
}
