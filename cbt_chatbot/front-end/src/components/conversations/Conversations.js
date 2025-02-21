import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Conversations.css';
import axiosInstance from '../utils/axios';

const Conversations = () => {
  const [conversations, setConversations] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchConversations = async () => {
      const token = localStorage.getItem('accessToken');
      if (!token) {
        console.error("No access token found");
        return;
      }
      try {
        const response = await axiosInstance.get('http://localhost:8000/api/conversations/', {
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
    console.log(`Deleting Conversation with ID:  ${conversationId}`)
    const token = localStorage.getItem('accessToken');
    if (!token) {
      console.error("No access token found");
      return;
    }
    try {
      await axiosInstance.delete(`http://localhost:8000/api/conversations/${conversationId}/`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setConversations(conversations.filter(conversation => conversation.id !== conversationId));
    } catch (error) {
      console.error('Error deleting conversation:', error.response ? error.response.data : error.message);
    }
  };

  const handleResumeConversation = (conversationId) => {
    console.log(`Resuming conversation with ID: ${conversationId}`);
    navigate(`/sessions/chatbot`, { state: { convoId: conversationId } });
  };

  const handViewConversation = (conversationId) => {
    console.log(`Viewing conversation with ID: ${conversationId}`);
    navigate(`/conversations/${conversationId}`);
  };

  return (
    <div className="conversations-container">
      <h1>Your Conversations</h1>
      {conversations.length === 0 ? (
        <div className="no-conversations">
          <p>You have no previous conversations.</p>
        </div>
      ) : (
        <ul>
          {conversations.map(conversation => (
            <li key={conversation.id} className="conversation-item">
              <div className="conversation-title">{conversation.title}</div>
              <div>
                <button onClick={() => handViewConversation(conversation.id)}>View</button>
                <button onClick={() => handleResumeConversation(conversation.id)}>Resume</button>
                <button onClick={() => handleDeleteConversation(conversation.id)}>Delete</button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Conversations;