import React from 'react'
import { Project } from './project';
import AccountTreeIcon from '@mui/icons-material/AccountTree';

export const ProjectTemplate = (props) =>{
    return (
        <div style={{display:"flex", flexDirection:"column"}}>
			{props.projects.length === 0 ? (
				'No projects to display'
			) : (
				props.projects.map((project) => {
					return <Project {...props} project={project} key={project.id} />;
				})
			)}
		</div>
    );
}