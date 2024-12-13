import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import "./App.css"
import Chatbot from '../chatbot/Chatbot';
import Home from '../home/Home'
import Login from '../login/Login';
import Register from '../register/Register';

function App() {
  return (
    <Router>
      <nav>
        <ul>
          <li><Link to="/">Home</Link></li>
          <li><Link to="/chatbot">Chatbot</Link></li>
          <li><Link to="/login">Login</Link></li>
          <li><Link to="/register">Register</Link></li>
        </ul>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/chatbot" element={<Chatbot />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </Router>
  );
}

export default App;