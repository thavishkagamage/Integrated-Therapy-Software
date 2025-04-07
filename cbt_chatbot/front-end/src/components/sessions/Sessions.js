import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../conversations/Conversations.css';

const Sessions = () => {
	const [isLoggedIn, setIsLoggedIn] = useState(false);
	const navigate = useNavigate();
	const sessions = Array.from({ length: 1 }, (_, index) => index + 1);

	useEffect(() => {
		const token = localStorage.getItem('accessToken');
		if (token) {
			setIsLoggedIn(true);
		}
	}, []);

	const handleStartConversation = (session) => {
		if (isLoggedIn) {
			console.log(`Starting CBT session number: ${session}`);
			navigate(`/sessions/chatbot/${session}`);
		} else {
			navigate('/login'); // Redirect to login if not logged in
		}
	};
	
	return (
		<div className="sessions-container">
			<h1 className='mb-4 font-bold'>CBT Sessions</h1>
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
			<span className="text-lg font-bold italic">More sessions coming soon...</span>
		</div>
	)
}

export default Sessions;