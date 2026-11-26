import React, { createContext, useState, useContext, ReactNode, useEffect } from 'react'
import { AuthContextType, UserProfile } from './types'
import { apiClient } from './api'

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [olmId, setOlmId] = useState<string | null>(null)
  const [user, setUser] = useState<UserProfile | null>(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  // Initialize session from localStorage on mount
  useEffect(() => {
    const token = localStorage.getItem('access_token')
    const storedOlmId = localStorage.getItem('olm_id')
    const storedUser = localStorage.getItem('user_profile')

    if (token && storedOlmId) {
      setOlmId(storedOlmId)
      if (storedUser) {
        try {
          setUser(JSON.parse(storedUser))
        } catch {
          // ignore parsing error
        }
      }
      setIsAuthenticated(true)
    }
  }, [])

  const login = async (id: string, password: string) => {
    const data = await apiClient.login(id, password)
    localStorage.setItem('access_token', data.access_token)
    localStorage.setItem('olm_id', data.user.olm_id)
    localStorage.setItem('user_profile', JSON.stringify(data.user))
    setOlmId(data.user.olm_id)
    setUser(data.user)
    setIsAuthenticated(true)
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('olm_id')
    localStorage.removeItem('user_profile')
    setOlmId(null)
    setUser(null)
    setIsAuthenticated(false)
  }

  return (
    <AuthContext.Provider value={{ olmId, user, isAuthenticated, login, logout }}>
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
