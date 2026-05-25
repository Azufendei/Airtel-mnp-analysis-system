import React from 'react'
import { MNPJourneyEvent } from './types'
import { format } from 'date-fns'
import './JourneyTable.css'

interface JourneyTableProps {
  events: MNPJourneyEvent[]
}

export default function JourneyTable({ events }: JourneyTableProps) {
  const getStatusClass = (result: string) => {
    return result.toLowerCase() === 'success' ? 'status-success' : 'status-failed'
  }

  const getEventIcon = (eventType: string) => {
    const icons: Record<string, string> = {
      'Port_in': '📥',
      'Port_out': '📤',
      'UPC': '📋',
      'NPD_IN': '✓',
      'NPD_Out': '✓',
      'Number_return': '↩️'
    }
    return icons[eventType] || '●'
  }

  return (
    <div className="journey-table-container">
      {events.length === 0 ? (
        <div className="no-data">No journey events found for this MSISDN</div>
      ) : (
        <div className="table-wrapper">
          <table className="journey-table">
            <thead>
              <tr>
                <th>Event Type</th>
                <th>Timestamp</th>
                <th>Operator</th>
                <th>Circle</th>
                <th>Result</th>
                <th>Transaction ID</th>
                <th>Details</th>
              </tr>
            </thead>
            <tbody>
              {events.map((event, idx) => (
                <tr key={idx} className="event-row">
                  <td className="event-type">
                    <span className="event-icon">{getEventIcon(event.event_type)}</span>
                    {event.event_type.replace(/_/g, ' ')}
                  </td>
                  <td className="timestamp">
                    {format(new Date(event.timestamp), 'dd/MM/yyyy HH:mm:ss')}
                  </td>
                  <td className="operator">{event.operator}</td>
                  <td className="circle">{event.circle}</td>
                  <td className={`result ${getStatusClass(event.result)}`}>
                    {event.result}
                  </td>
                  <td className="txn-id">
                    <code>{event.txn_id}</code>
                  </td>
                  <td className="details">
                    {Object.keys(event.details).length > 0 ? (
                      <details>
                        <summary>View</summary>
                        <pre>{JSON.stringify(event.details, null, 2)}</pre>
                      </details>
                    ) : (
                      '-'
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
