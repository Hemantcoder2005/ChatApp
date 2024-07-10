import axios from 'axios'
import React from 'react'
import {useNavigate} from 'react-router-dom'

const useRegister = () => {
    const navigate = useNavigate()
  const registerHook = (data) => {
    axios.post("http://127.0.0.1:8000/api/accounts/register/", data)
    .then((respo) => {
        if (!respo.data.error) {
            navigate('/login')
        }else{
            console.log(respo.data.mssg)
        }
    })
    .catch((error) => {
        console.log(error)
    })
  }

  return {registerHook}
}

export default useRegister
