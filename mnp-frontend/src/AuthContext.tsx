import React, { createContext, useState, useContext, ReactNode, useEffect } from 'react'
import { AuthContextType } from './types'

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [olmId, setOlmId] = useState<string | null>(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  // Initialize from localStorage on mount
  useEffect(() => {
    const storedOlmId = localStorage.getItem('olm_id')
    if (storedOlmId) {
      setOlmId(storedOlmId)
      setIsAuthenticated(true)
    }
  }, [])

  const login = (olmId: string) => {
    setOlmId(olmId)
    setIsAuthenticated(true)
    localStorage.setItem('olm_id', olmId)
  }

  const logout = () => {
    setOlmId(null)
    setIsAuthenticated(false)
    localStorage.removeItem('olm_id')
  }

  return (
    <AuthContext.Provider value={{ olmId, isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
