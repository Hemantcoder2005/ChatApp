import React from 'react'
import axios from 'axios'
import { useAuthStore } from '../context/store'


const useLogin = () => {
    const {login} = useAuthStore()
 const loginHook = (data) => {
    axios.post('http://127.0.0.1:8000/api/accounts/login/', data)
    .then((respo) => {
        console.log(respo.data)
        localStorage.setItem('chat-client', JSON.stringify(respo.data))
        login(respo.data)
    })
    .catch((error) => {
        console.log(error)
 })
 }

 return {loginHook}
}

export default useLogin
