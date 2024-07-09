import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Home = () => {

    const [data, setData] = useState("")
    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/')
            .then(respo => {
                setData(respo.data.message)
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }, []);

    return (
        <div>
            <h1>Hello, world! {data}</h1>
        </div>
    );
};

export default Home;
