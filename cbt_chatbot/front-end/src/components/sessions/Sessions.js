import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../conversations/Conversations.css';

const Sessions = () => {
	
	const navigate = useNavigate();
	const sessions = Array.from({ length: 3 }, (_, index) => index + 1);

	const handleStartConversation = (session) => {
		console.log(`Starting CBT session number: ${session}`);
		navigate(`/sessions/chatbot/${session}`);
	};
	
	return (
		<div className="sessions-container">
		<h1>CBT Sessions</h1>
		<ul>
			<li className="conversation-item">
				<div className="conversation-title">Free Chat</div>
				<div>
					<button onClick={() => handleStartConversation(0)}>Start</button>
				</div>
			</li>

			{sessions.map(session => (
				<li key={session} className="conversation-item">
					<div className="conversation-title">Session {session}</div>
					<div>
						<button onClick={() => handleStartConversation(session)}>Start</button>
					</div>
				</li>
			))}
		</ul>
		</div>
	)
}

export default Sessions;