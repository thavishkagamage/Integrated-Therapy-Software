import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const Conversations = () => {
  const [conversations, setConversations] = useState([]);

  useEffect(() => {
    const fetchConversations = async () => {
      const token = localStorage.getItem('accessToken');
      if (!token) {
        console.error("No access token found");
        return;
      }
      try {
        const response = await axios.get('http://localhost:8000/api/conversations/', {
          headers: { Authorization: `Bearer ${token}` }
        });
        setConversations(response.data);
      } catch (error) {
        console.error('Error fetching conversations:', error.response ? error.response.data : error.message);
      }
    };

    fetchConversations();
  }, []);

  const handleDeleteConversation = async (conversationId) => {
    const token = localStorage.getItem('accessToken');
    if (!token) {
      console.error("No access token found");
      return;
    }
    try {
      await axios.delete(`http://localhost:8000/api/conversations/${conversationId}/`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setConversations(conversations.filter(conversation => conversation.id !== conversationId));
    } catch (error) {
      console.error('Error deleting conversation:', error.response ? error.response.data : error.message);
    }
  };

  return (
    <div>
      <h1>Your Conversations</h1>
      <ul>
        {conversations.map(conversation => (
          <li key={conversation.id}>
            <Link to={`/conversations/${conversation.id}`}>{conversation.title}</Link>
            <button onClick={() => handleDeleteConversation(conversation.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Conversations;