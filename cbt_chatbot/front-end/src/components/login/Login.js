import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import './Login.css';

const Login = ({ setIsLoggedIn }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            // Login existing user
            const response = await axios.post('https://therathrivebackend-dqhsf3gdc0b2dgey.canadacentral-01.azurewebsites.net/api/users/login/', {
                username,
                password,
            });
            localStorage.setItem('accessToken', response.data.access);
            localStorage.setItem('refreshToken', response.data.refresh);
            // Fetch user ID
            const userResponse = await axios.get('https://therathrivebackend-dqhsf3gdc0b2dgey.canadacentral-01.azurewebsites.net/api/users/me/', {
                headers: { Authorization: `Bearer ${response.data.access}` }
            });
            console.log('Login response:', userResponse.data); // For debugging purposes
            localStorage.setItem('userId', userResponse.data.user_id);
            localStorage.setItem('first_name', userResponse.data.first_name);

            setIsLoggedIn(true);
            alert('Login successful!');
            navigate('/');
        } catch (error) {
            console.error('Login failed:', error.response.data);
            alert('Invalid credentials');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-container">
            <form onSubmit={handleLogin} className="login-form">
                <h2 className="login-title">Login</h2>
                
                {error && <p className="login-error">{error}</p>}
                
                <div className="login-field">
                    <label className="login-label">Username:</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                        className="login-input"
                    />
                </div>

                <div className="login-field">
                    <label className="login-label">Password:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        className="login-input"
                    />
                </div>

                <button type="submit" disabled={loading} className="login-button">
                    {loading ? 'Logging in...' : 'Login'}
                </button>

                <div className="register-login-link">Don't have an account? <Link to="/register">Sign up</Link></div>
            </form>
        </div>
    );
};

export default Login;