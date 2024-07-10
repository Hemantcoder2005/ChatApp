import React from 'react'
import { Navigate } from 'react-router-dom'
import { useAuthStore } from '../context/store'

const ProtectedRoute = ({children}) => {
    const {user} = useAuthStore()
    if (!user || !user.jwt) {
        // If no user or accessToken is found, redirect to login
        return <Navigate to="/login" />
    }

    return children
}

export default ProtectedRoute
