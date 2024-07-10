import React, { useEffect, useState } from 'react';
import axios from 'axios';
import useLogout from '../hooks/useLogout';



const Home = () => {
    const { logoutHook } = useLogout()

    const handleLogout = () => {
        logoutHook()
    }


    return (
        <div>
            <h1>Hello, world! </h1>
            <button onClick={handleLogout}>Logout</button>
        </div>
    );
};

export default Home;
