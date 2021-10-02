import React, { useEffect } from 'react';
import { Redirect } from 'react-router';
import CreateList from './CreateList';
import axios from 'axios';
import {MyList} from './list'
import { Grid } from '@mui/material';
// Main Component
export class ListProject extends React.Component {
	constructor(props) {
		super(props);
		this.state = { projectContent: null };
		this.renderLists = this.renderLists.bind(this);
	}
	componentDidMount() {
		this.props.checkLoginStatus();
		this.props.getUser();
		this.renderLists();
	}
	renderLists() {
		axios
			.get('http://127.0.0.1:8000/trelloAPIs/projects/' + this.props.id, { withCredentials: true })
			.then((response) => {
				console.log('Inside list project');
				console.log(response.data);
				this.setState({ projectContent: response.data });
			})
			.catch((error) => {
				console.log(error);
			});
	}
	render() {
		console.log("id", this.props.id);
		if (this.props.loginStatus) {
			if(this.state.projectContent){
                console.log("content");
                console.log(this.state.projectContent);
                return (
                    <div>
                        <p>Project Number {this.state.projectContent.id}</p>
						<Grid container spacing={2}>
						{this.state.projectContent["project_lists"].map((list) => {
                        return <Grid item xs={6} md={4}>
								<MyList {...this.props} list={list} key={list.id} />
							</Grid>;
                    })}
						</Grid>
						<CreateList {...this.props} project={this.state.projectContent} renderLists={this.renderLists}></CreateList>
					</div>

                );
            }
            else{
                return <p>Loading Lists...</p>
            }
		} else {
			console.log('Inside listProject');
			return <Redirect to="/" />;
		}
	}
}
