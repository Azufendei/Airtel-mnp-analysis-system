import type { ReactNode, FC } from 'react'
import { useAuth } from './AuthContext'
import LoginPage from './LoginPage'

interface ProtectedRouteProps {
  children: ReactNode
}

export const ProtectedRoute: FC<ProtectedRouteProps> = ({ children }) => {
  const { isAuthenticated } = useAuth()

  if (!isAuthenticated) {
    return <LoginPage />
  }

  return <>{children}</>
}
