import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

const ConversationDetail = () => {
  const { id } = useParams();
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const fetchMessages = async () => {
      const token = localStorage.getItem('accessToken');
      if (!token) {
        console.error("No access token found");
        return;
      }
      try {
        const response = await axios.get(`http://localhost:8000/api/conversations/${id}/`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        setMessages(response.data.messages);
      } catch (error) {
        console.error('Error fetching messages:', error.response ? error.response.data : error.message);
      }
    };

    fetchMessages();
  }, [id]);

  return (
    <div className="chat-window">
      <h1>Conversation Messages</h1>
      <div className="chat-messages">
        {messages.map(message => (
          <span key={message.id} className={`${message.sender}-message message`}>
            {message.content}
          </span>
        ))}
      </div>
    </div>
  );
};

export default ConversationDetail;