import React, { useState } from 'react'
import { format, subDays } from 'date-fns'
import './SearchForm.css'

interface SearchFormProps {
  onSearch: (msisdn: string, startTime?: string, endTime?: string) => void
  loading: boolean
}

export default function SearchForm({ onSearch, loading }: SearchFormProps) {
  const [msisdn, setMsisdn] = useState('')
  const [useTimeRange, setUseTimeRange] = useState(false)
  const [startDate, setStartDate] = useState(format(subDays(new Date(), 7), 'yyyy-MM-dd'))
  const [endDate, setEndDate] = useState(format(new Date(), 'yyyy-MM-dd'))
  const [error, setError] = useState('')

  const validateMsisdn = (value: string): boolean => {
    // Indian MSISDN format: 10 digits starting with 9, or +91 prefix
    const msisdnRegex = /^(\+91)?[6-9]\d{9}$/
    return msisdnRegex.test(value.replace(/\D/g, ''))
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    if (!msisdn.trim()) {
      setError('Please enter an MSISDN')
      return
    }

    if (!validateMsisdn(msisdn)) {
      setError('Invalid MSISDN format. Please enter a valid Indian mobile number.')
      return
    }

    const cleanMsisdn = msisdn.replace(/\D/g, '')
    const formattedMsisdn = cleanMsisdn.length === 10 ? '91' + cleanMsisdn : cleanMsisdn

    if (useTimeRange) {
      const startTime = new Date(startDate).toISOString()
      const endTime = new Date(endDate).toISOString()

      if (new Date(startDate) >= new Date(endDate)) {
        setError('Start date must be before end date')
        return
      }

      onSearch(formattedMsisdn, startTime, endTime)
    } else {
      onSearch(formattedMsisdn)
    }
  }

  return (
    <div className="search-form-container">
      <form onSubmit={handleSubmit} className="search-form">
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="msisdn">MSISDN</label>
            <input
              id="msisdn"
              type="text"
              placeholder="Enter mobile number (10 or 13 digits)"
              value={msisdn}
              onChange={(e) => setMsisdn(e.target.value)}
              disabled={loading}
              className="form-input"
            />
          </div>
        </div>

        <div className="form-row">
          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={useTimeRange}
              onChange={(e) => setUseTimeRange(e.target.checked)}
              disabled={loading}
            />
            Use Date Range
          </label>
        </div>

        {useTimeRange && (
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="startDate">Start Date</label>
              <input
                id="startDate"
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                disabled={loading}
                className="form-input"
              />
            </div>
            <div className="form-group">
              <label htmlFor="endDate">End Date</label>
              <input
                id="endDate"
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                disabled={loading}
                className="form-input"
              />
            </div>
          </div>
        )}

        {error && <div className="error-message">{error}</div>}

        <button
          type="submit"
          disabled={loading}
          className="submit-button"
        >
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>
      </form>
    </div>
  )
}
