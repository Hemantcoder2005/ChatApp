import React from 'react'
import { useNavigate } from 'react-router-dom'


const useLogout = () => {
    const navigate = useNavigate()
    const logoutHook = () => {
        localStorage.removeItem('chat-client')
        navigate('/login')
    }
  return{logoutHook}
}

export default useLogout
