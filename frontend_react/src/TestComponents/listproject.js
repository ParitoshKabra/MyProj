import React, { useEffect } from 'react';
import { Redirect } from 'react-router';
import axios from 'axios';
import {MyList} from './list'

export class ListProject extends React.Component {
	constructor(props) {
		super(props);
		this.state = { projectContent: null };
		this.renderLists = this.renderLists.bind(this);
	}
	componentDidMount() {
		this.props.checkLoginStatus();
		this.renderLists();
	}
	renderLists() {
		axios
			.get('http://127.0.0.1:8000/trelloAPIs/projects/' + this.props.match.params.id, { withCredentials: true })
			.then((response) => {
				console.log('Inside list project');
				console.log(response.data);
				this.setState({ projectContent: response.data });
				return response.data;
			})
			.catch((error) => {
				console.log(error);
				return error;
			});
	}
	render() {
		if (this.props.loginStatus) {
			if(this.state.projectContent){
                console.log("content");
                console.log(this.state.projectContent);
                return (
                    <div>
                        <p>Project Number {this.state.projectContent.id}</p>
                        {this.state.projectContent["project_lists"].map((list) => {
                        return <MyList {...this.props} list={list} key={list.id} />;
                    })}
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