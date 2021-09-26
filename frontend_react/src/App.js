import './App.css';
import {Login} from "./TestComponents/login";
import {Welcome} from "./TestComponents/welcome";
import {Omniport} from "./TestComponents/omniport";
import axios from 'axios';
import { useState, useEffect } from 'react';
import {
	BrowserRouter as Router,
	Switch,
	Route,
  Redirect
  } from "react-router-dom";

// How to access here

function App() {
  
  const [loggedin, setLoggedin] = useState(false);
  
  const checkLoginStatus = ()=>{
    axios
    .get("http://127.0.0.1:8000/trelloAPIs/check_login")
    .then(response =>{
      console.log(response)
      if(response.data.loggedin === true && loggedin === false){
          setLoggedin(true);
      }
      else if(loggedin === true && response.data.loggedin === false){
          setLoggedin(false);
      }
    })
    .catch(error =>{
      console.log("checking error...", error);
    });
  }

  useEffect(()=>{
    checkLoginStatus();
  }, []);
  
    console.log(loggedin)
    return (
      <Router>
          <h1>Trello App</h1>
          <Route exact path = "/" render = {() =>{
            return <Login loginStatus = {loggedin}/>
          }}/>
          <Route exact path="/login/success" render = {() =>{
            return <Welcome loginStatus = {loggedin}/>
          }}/>
          <Route exact path="/omniport" component={Omniport}/>
      </Router>
    );
}

export default App;
