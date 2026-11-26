import { AuthProvider, useAuth } from './AuthContext'
import LoginPage from './LoginPage'
import Dashboard from './Dashboard'
import './App.css'

function AppContent() {
  const { isAuthenticated } = useAuth()

  return isAuthenticated ? <Dashboard /> : <LoginPage />
}

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  )
}
