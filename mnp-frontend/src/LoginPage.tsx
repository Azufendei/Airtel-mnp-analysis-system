import React, { useState } from 'react'
import { useAuth } from './AuthContext'
import './LoginPage.css'

export default function LoginPage() {
  const [olmId, setOlmId] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { isAuthenticated, login } = useAuth()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      if (!olmId.trim() || !password.trim()) {
        setError('Please enter both your OLM ID and Password')
        setLoading(false)
        return
      }

      await login(olmId.trim(), password)
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Authentication failed. Please verify your OLM credentials.'
      setError(msg)
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
          <p>Enterprise Telecom Portability Analytics</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="olmId">OLM Operator ID</label>
            <input
              id="olmId"
              type="text"
              placeholder="e.g. OLM_ADMIN_001"
              value={olmId}
              onChange={(e) => setOlmId(e.target.value)}
              disabled={loading}
              className="form-input"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              placeholder="Enter password (Default: Password@123)"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={loading}
              className="form-input"
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <button
            type="submit"
            disabled={loading || !olmId.trim() || !password.trim()}
            className="submit-button"
          >
            {loading ? 'Authenticating...' : 'Sign In'}
          </button>
        </form>

        <div className="login-footer">
          <p>Protected by OAuth2 / JWT. Default credentials: <code>Password@123</code></p>
        </div>
      </div>
    </div>
  )
}
