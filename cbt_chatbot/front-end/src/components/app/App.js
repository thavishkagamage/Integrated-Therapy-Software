import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import axiosInstance from '../utils/axios';
import "./App.css";
import Chatbot from '../chatbot/Chatbot';
import Home from '../home/Home';
import Login from '../login/Login';
import Register from '../register/Register';
import Conversations from '../conversations/Conversations';
import ConversationDetail from '../conversations/ConversationDetail';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      setIsLoggedIn(true);
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    setIsLoggedIn(false);
  };

  const handleClearConversations = async () => {
    const token = localStorage.getItem('accessToken');
    if (!token) {
      console.error("No access token found");
      return;
    }
    try {
      await axiosInstance.delete('clear_conversations/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      alert('All conversations cleared!');
    } catch (error) {
      console.error('Error clearing conversations:', error.response ? error.response.data : error.message);
    }
  };

  return (
    <Router>
      <nav>
        <ul>
          <li><Link to="/">Home</Link></li>
          <li><Link to="/chatbot">Chatbot</Link></li>
          {isLoggedIn && <li><Link to="/conversations">Conversations</Link></li>}
          {!isLoggedIn && <li><Link to="/login">Login</Link></li>}
          {!isLoggedIn && <li><Link to="/register">Register</Link></li>}
          {isLoggedIn && <li><button onClick={handleLogout}>Logout</button></li>}
          {isLoggedIn && <li><button onClick={handleClearConversations}>Clear All Conversations</button></li>}
        </ul>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/chatbot" element={<Chatbot />} />
        <Route path="/conversations" element={<Conversations />} />
        <Route path="/conversations/:id" element={<ConversationDetail />} />
        <Route path="/login" element={<Login setIsLoggedIn={setIsLoggedIn} />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </Router>
  );
}

export default App;