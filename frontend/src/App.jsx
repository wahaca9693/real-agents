import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useState, createContext, useContext } from 'react'
import Landing from './pages/Landing'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import ChatPage from './pages/ChatPage'
import Settings from './pages/Settings'
import ProfileSettings from './pages/ProfileSettings'
import ModelsSettings from './pages/ModelsSettings'
import AppearanceSettings from './pages/AppearanceSettings'
import { ToastProvider } from './components/Toast'
import './index.css'

// Auth Context
const AuthContext = createContext(null)

export function useAuth() {
  return useContext(AuthContext)
}

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(true) // Default true for demo

  return (
    <AuthContext.Provider value={{ isAuthenticated, setIsAuthenticated }}>
      <ToastProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route 
              path="/app" 
              element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" />} 
            />
            <Route 
              path="/app/chat/:id" 
              element={isAuthenticated ? <ChatPage /> : <Navigate to="/login" />} 
            />
            <Route path="/app/settings" element={<Settings />} />
            <Route path="/app/settings/profile" element={<ProfileSettings />} />
            <Route path="/app/settings/models" element={<ModelsSettings />} />
            <Route path="/app/settings/appearance" element={<AppearanceSettings />} />
          </Routes>
        </BrowserRouter>
      </ToastProvider>
    </AuthContext.Provider>
  )
}

export default App