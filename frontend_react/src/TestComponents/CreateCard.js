import React from 'react';
import TextField from '@mui/material/TextField';
import { MenuItem } from '@mui/material';
import Button from '@mui/material/Button';
import { Box } from '@mui/material';
import { useState, useEffect } from 'react';
import axios from 'axios';
// import AdapterDateFns from '@mui/lab/AdapterDateFns';
// import LocalizationProvider from '@mui/lab/LocalizationProvider';

export const CreateCard = (props) => {
	// const [card, setcard] = useState({"card_list"})
	const [ title, setTitle ] = useState('');
	const [ errorTitle, setErrorTitle ] = useState(false);
	const [ errormsg, setErrorMsg ] = useState('');
	const [ descp, setDescp ] = useState('');
	const [ datetime, setDateTime ] = useState(new Date());
	const [ assigned_to, setAssigned_to ] = useState([]);
	const [members, setMembers] = useState([]);
	// created_by, list
	console.log(props);
	const handleCreateCard = async (e) => {
		e.preventDefault();
		setErrorTitle(false);
		console.log(title, descp);
		if (title === '') {
			setErrorMsg('Required');
			setErrorTitle(true);
		} else {
			const res = await axios
				.get('http://127.0.0.1:8000/trelloAPIs/lists/' + props.match.params.id, { withCredentials: true })
				.then((response) => {
					console.log(response.data);
					return response.data;
				})
				.catch((error) => {
					console.log(error);
					return error;
				});
			res.list_cards.forEach((item) => {
				if (title === item.title) {
					setErrorMsg('Choose a different title');
					setErrorTitle(true);
				}
			});
		}
	};
	const getMembers = async () => {
		const res = await axios
			.get('http://127.0.0.1:8000/trelloAPIs/projects/' + props.match.params.projectid, { withCredentials: true })
			.then((response) => {
				console.log(response.data);
				return response.data;
			})
			.catch((error) => {
				console.log(error);
				return error;
			});
		setMembers(res.members);
	};
	useEffect(getMembers, [members]);
	return (
		<Box
			component="form"
			sx={{
				display: 'flex',
				flexDirection: 'column',
				'& > :not(style)': { m: 1, width: '25ch' }
			}}
			noValidate
			autoComplete="off"
		>
			<TextField
				id="filled-basic"
				label="Title"
				variant="outlined"
				color="secondary"
				InputLabelProps={{
					shrink: true
				}}
				onChange={(e) => setTitle(e.target.value)}
				error={errorTitle}
				helperText={errormsg}
			/>
			<TextField
				id="standard-multiline-flexible"
				label="Description"
				variant="outlined"
				color="secondary"
				InputLabelProps={{
					shrink: true
				}}
				multiline
				onChange={(e) => setDescp(e.target.value)}
				rows={4}
			/>
			<TextField
				id="datetime-local"
				label="Due-Date"
				type="datetime-local"
				InputLabelProps={{
					shrink: true
				}}
				variant="outlined"
				color="secondary"
				sx={{ width: 250 }}
				onchange={(e) => {
					setDateTime(e.target.value);
				}}
			/>
			<TextField
				id="filled-select-currency"
				select
				color="secondary"
				label="Assign To:"
				onChange={(e) => {
					console.log(e.target.value);
					setAssigned_to(e.target.value);
				}}
				helperText="assign cards to project members"
				variant="filled"
			>
				{members.map((option) => (
					<MenuItem key={option} value={option}>
						{option.label}
					</MenuItem>
				))}
			</TextField>
			<Button variant="contained" color="secondary" type="submit" onClick={handleCreateCard}>
				Submit
			</Button>
		</Box>
	);
};
