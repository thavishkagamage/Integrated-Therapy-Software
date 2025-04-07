import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Conversations.css';
import axiosInstance from '../utils/axios';

const Conversations = () => {
  const [conversations, setConversations] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('accessToken');
    if (!token) {
      navigate('/login'); // Redirect to login if no token found
    }

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

  // Calculate indices for the current page's items
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentConversations = conversations.slice(indexOfFirstItem, indexOfLastItem);

  // Calculate total pages
  const totalPages = Math.ceil(conversations.length / itemsPerPage);

  const handleNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage(prevPage => prevPage + 1);
    }
  };

  const handlePrevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(prevPage => prevPage - 1);
    }
  };

  const handleDeleteConversation = async (conversationId) => {
    console.log(`Deleting Conversation with ID: ${conversationId}`);
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

  const handleResumeConversation = (conversationId, sessionNumber) => {
    console.log(`Resuming conversation with ID: ${conversationId}`);
    navigate(`/sessions/chatbot/${sessionNumber}/${conversationId}`);
  };

  const handViewConversation = (conversationId) => {
    console.log(`Viewing conversation with ID: ${conversationId}`);
    navigate(`/conversations/${conversationId}`);
  };

  return (
    <div className="conversations-container">
      <h1 className="font-bold mb-4">Your Conversations</h1>
      {conversations.length === 0 ? (
        <div className="no-conversations">
          <p>You have no previous conversations.</p>
        </div>
      ) : (
        <>
          <ul>
            {currentConversations.map(conversation => (
              <li key={conversation.id} className="conversation-item flex justify-between items-center p-4 border-b">
                <div className="conversation-title">{conversation.title}</div>
                <div className="buttons-container">
                  <button onClick={() => handViewConversation(conversation.id)} className="bg-green-500 hover:bg-green-700 text-white font-bold py-1 px-3 rounded">
                    View
                  </button>
                  <button onClick={() => handleResumeConversation(conversation.id, conversation.session_number)} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-1 px-3 rounded">
                    Resume
                  </button>
                  <button onClick={() => handleDeleteConversation(conversation.id)} className="bg-red-500 hover:bg-red-700 text-white font-bold py-1 px-3 rounded">
                    Delete
                  </button>
                </div>
              </li>
            ))}
          </ul>
          <div className="pagination-controls flex justify-center items-center space-x-4 mt-4">
            <button 
              onClick={handlePrevPage} 
              disabled={currentPage === 1}
              className="bg---highlight-color hover:bg-accent-color text-white font-bold py-2 px-4 rounded disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            <span className="text-gray-700 font-medium">
              Page {currentPage} of {totalPages}
            </span>
            <button 
              onClick={handleNextPage} 
              disabled={currentPage === totalPages}
              className="bg---highlight-color hover:bg-accent-color text-white font-bold py-2 px-4 rounded disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default Conversations;
