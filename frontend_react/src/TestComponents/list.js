import axios from 'axios';
import React from 'react';
import { useState, useEffect } from 'react';
import Button from '@material-ui/core/Button';
import Stack from '@mui/material/Stack';
import EditRoundedIcon from '@mui/icons-material/EditRounded';
import { makeStyles } from '@material-ui/core';
import { Typography } from '@material-ui/core';
import AddCircleIcon from '@material-ui/icons/Add';
import { ButtonGroup } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import { ListItemText } from '@material-ui/core';
import { ListItem } from '@mui/material';
import VisibilityIcon from '@mui/icons-material/Visibility';
import { Dialog, DialogTitle, DialogContent } from '@material-ui/core';
import { CreateCard } from './CreateCard';

const useStyles = makeStyles({
	btn: {
		fontSize: '16px',
		border: '50%'
	},
	container: {
		maxWidth: '148px',
		maxHeight: '200px',
		overflow: 'auto',
		border: '2px solid red'
	}
});

export const MyList = (props) => {
	const classes = useStyles();
	const [ listContent, setlistContent ] = useState({});
	const [ editCard, setEditCard ] = useState(false);
	const [cardUnderEdit, setCardUnderEdit] = useState({});

	const getList = () => {
		axios
			.get('http://127.0.0.1:8000/trelloAPIs/lists/' + props.list.id, { withCredentials: true })
			.then((response) => {
				console.log('Inside list');
				console.log(response.data);
				setlistContent(response.data);
			})
			.catch((error) => {
				console.log(error);
			});
	};

	useEffect(() => {
		getList();
	}, []);

	const EditCard = (card) => {
		setEditCard(true);
		setCardUnderEdit(card);
	};
	const ViewCard = () => {};
	
	const handleClose = () => {
		setEditCard(false);
	};
	if (listContent) {
		console.log(listContent['list_cards']);
		let cards;
		if (listContent['list_cards']) {
			cards = listContent.list_cards.map((card) => {
				return (
					<ListItem>
						<ListItemText primary={card.title} />
						<ButtonGroup key={card.id}>
							<Button
								variant="outlined"
								onClick={(e) =>{EditCard(card);}}
								color="secondary"
								startIcon={<EditRoundedIcon />}
							/>
							<Button
								variant="outlined"
								onClick={ViewCard}
								color="secondary"
								startIcon={<VisibilityIcon />}
							/>
						</ButtonGroup>
					</ListItem>
				);
			});
		} else {
			cards = 'Loading cards...';
		}
		return (
			<Stack spacing={2} className={classes.conatainer}>
				<Typography variant="h6" gutterBottom align="center">
					{listContent.title}
				</Typography>
				<Stack spacing={1.2}>{cards}</Stack>

				<ButtonGroup>
					<Button
						color="primary"
						variant="outlined"
						className={classes.btn}
						onClick={() => {
							props.history.push('/createCard/' + props.list.id + '/' + props.list.lists_project);
						}}
					>
						<AddCircleIcon />
					</Button>
					<Button
						color="secondary"
						variant="contained"
						onClick={() => {
							props.axiosInstance
								.delete('http://127.0.0.1:8000/trelloAPIs/lists/' + props.list.id + '/', {
									withCredentials: true
								})
								.then((res) => {
									console.log('List deleted successfully!', res);
									props.renderLists();
								})
								.catch((error) => {
									console.log(error);
								});
						}}
					>
						<DeleteIcon />
					</Button>
				</ButtonGroup>
				<Dialog onClose={handleClose} open={editCard}>
					<DialogTitle>Edit Card</DialogTitle>
					<DialogContent>
						<CreateCard {...props} edit={editCard} card={cardUnderEdit} handleClose={handleClose}></CreateCard>
					</DialogContent> 
				</Dialog>
			</Stack>
		);
	} else {
		return <div>Loading List...</div>;
	}
};
