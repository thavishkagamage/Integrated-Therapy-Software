import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import axiosInstance from '../utils/axios';
import "./App.css";
import Chatbot from '../chatbot/Chatbot';
import Sessions from '../sessions/Sessions';
import Home from '../home/Home';
import Login from '../login/Login';
import Register from '../register/Register';
import Conversations from '../conversations/Conversations';
import ConversationDetail from '../conversations/ConversationDetail';
import Goals from '../goals/Goals';  
import Teams from '../teams/Teams';
import UserIcon from "../../images/user-icon.png";
import Profile from '../profile/Profile';

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
    <div className="content-container">
      <Router>
        <header className="header"> 
          <nav className="nav-bar">
          <Link to="/" className="app-logo">
          <img src="/TheraThrive1.png" alt="TheraThrive Logo" className="logo-img" style={{ width: "300px", height: "auto" }}/>
          </Link>


          <ul className="nav-list">
            <li className="nav-item"><Link className="nav-link" to="/sessions">Chat</Link></li>
            {isLoggedIn && <li className="nav-item"><Link className="nav-link" to="/conversations">Conversations</Link></li>}
            {isLoggedIn && <li className="nav-item"><Link className="nav-link" to="/goals">Goals</Link></li>}
            {isLoggedIn && <li className="nav-item"><Link className="nav-link" to="/teams">Meet the Team</Link></li>}  {/* <-- Step 3 */}
          </ul>
            <div className="user-state-container">
              {isLoggedIn ? (
                <Link className="user-state" to="/profile">
                  <img className="user-icon" src={UserIcon} alt="User Icon" />
                  <span className="user-state-text">Profile</span>
                </Link>
              ) : (
                <Link className="user-state" to="/login">
                  <img className="user-icon" src={UserIcon} alt="User Icon" />
                  <span className="user-state-text">Login</span>
                </Link>
              )}
            </div>
          </nav>
        </header>
        <div className="main-content-container">
          {/* <aside className="left-aside"></aside> */}
<main>
  <Routes>
    <Route path="/" element={<Home />} />
    <Route path="/sessions" element={<Sessions />} />
    <Route path="/sessions/chatbot" element={<Chatbot />} />
    <Route path="/sessions/chatbot/:sessionId" element={<Chatbot />} />
    <Route path="/sessions/chatbot/:sessionId/:conversationId" element={<Chatbot />} />
    <Route path="/conversations" element={<Conversations />} />
    <Route path="/conversations/:id" element={<ConversationDetail />} />
    <Route path="/login" element={<Login setIsLoggedIn={setIsLoggedIn} />} />
    <Route path="/register" element={<Register setIsLoggedIn={setIsLoggedIn} />} />
    <Route path="/profile" element={<Profile handleLogout={handleLogout} />} />
    <Route path="/goals" element={<Goals />} />
    <Route path="/teams" element={<Teams />} />
  </Routes>
</main>

          {/* <aside className="right-aside"></aside> */}
        </div>
        {/* <div className="footer"></div> */}
      </Router>
    </div>
  );
}

export default App;
