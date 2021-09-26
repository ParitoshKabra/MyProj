import React, { useEffect } from 'react'
import axios from 'axios';


export const Omniport = (props)=>{
    const  getCode = async ()=>{
        const params = new URLSearchParams(window.location.search);
        // code = params.get("code")
        const auth = params.get("code")
        const user = await axios
        .get('http://127.0.0.1:8000/trelloAPIs/oauth_redirect', {params: {code:auth}}, {withCredentials: true})
        .then(response=>{
            console.log(response)
            return response.data
        })
        .catch(error=>{console.log("error occured with...", error)});
        console.log(user);
    }
    useEffect(()=>{
        getCode();
    }, [])
    return (
        <p>omniport authentication!!</p>
    );
}