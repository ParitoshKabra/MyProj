import axios from 'axios';
import React from 'react';
import { useState, useEffect } from 'react';
import { Redirect } from 'react-router';

export const Welcome = (props) => {
	const [ user, setUser ] = useState({});

	const getUser = () => {
		if (props.loginStatus) {
			axios
				.get('http://127.0.0.1:8000/trelloAPIs/user')
				.then((res) => {
					console.log(res);
					setUser(res.data[0]);
				})
				.catch((error) => {
					console.log(error);
				});
		}
		else{
			setUser({});
		}
	};
	useEffect(getUser, []);
	if (props.loginStatus) {
		// Design starts here 
		/* Welcome page should set the grid layout and then every component individually should be implemented, like Projects, Comments, Assigned_Cards, and the Dashboard then to be decided at the end*/ 
		return <h3>Welcome {user['username']}</h3>;
	} else {
		return <Redirect to="/" />;
	}
};
