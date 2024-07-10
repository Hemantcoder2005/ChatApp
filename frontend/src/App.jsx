import React, { useEffect } from 'react'
import {BrowserRouter as Router, Routes, Route, Navigate} from "react-router-dom"
import Login from './pages/Login'
import Home from './pages/Home'
import Register from './pages/Register'
import ProtectedRoute from './components/ProtectedRoute'
import { useAuthStore } from './context/store'




const App = () => {
  const {validateToken, user} = useAuthStore()

  useEffect(() => {
    validateToken();
  })
  return (
    <Router>
      <Routes>
        <Route path='/' element={<ProtectedRoute><Home /></ProtectedRoute>} />
        <Route path='/login' element={!user ? <Login /> : <Navigate to="/" />} />
        <Route path='/register' element={!user ? <Register /> : <Navigate to="/" />} />
      </Routes>
    </Router>
  )
}

export default App
