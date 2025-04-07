import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../login/Login.css';

const Register = ({ setIsLoggedIn }) => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [firstName, setFirstName] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleRegister = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        
        try {
            // Register new user
            await axios.post('https://therathrivebackend-dqhsf3gdc0b2dgey.canadacentral-01.azurewebsites.net/api/users/register/', {
                username,
                email,
                password,
                first_name: firstName,
            });
            // Login new user
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
            console.log('Registration and login response:', userResponse.data); // For debugging purposes
            localStorage.setItem('userId', userResponse.data.user_id);
            localStorage.setItem('first_name', response.data.first_name);

            setIsLoggedIn(true);
            alert('Registration successful!');
            navigate('/');
        } catch (error) {
            console.error('Registration failed:', error.response.data);
            if (error.response && error.response.data) {
                const errors = error.response.data;
                let errorMessage = '';
                if (errors.username && errors.email) {
                    errorMessage = 'A user with that username and email already exists.';
                } 
                else if (errors.username) {
                    errorMessage = errors.username;
                }
                else if (errors.email) {
                    errorMessage = errors.email;
                }
                // Fallback message if there are no specific errors
                else {
                    errorMessage = 'Error during registration. Please try again.';
                }
                setError(errorMessage);
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-container">
            <form onSubmit={handleRegister} className="login-form">
                <h2 className="login-title">Register</h2>
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
                    <label className="login-label">
                        First Name:
                        <div className="tooltip-wrapper">
                            <span className="info-icon">ℹ️</span>
                            <div className="tooltip-text">This is how the chatbot will address you.</div>
                        </div>
                    </label>
                    <input
                        type="text"
                        value={firstName}
                        onChange={(e) => setFirstName(e.target.value)}
                        required
                        className="login-input"
                    />
                </div>
                <div className="login-field">
                    <label className="login-label">Email:</label>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
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
                    {loading ? 'Registering...' : 'Register'}
                </button>

                <div className="register-login-link">Already have an account? <Link to="/login">Login</Link></div>
            </form>
        </div>
    );
};

export default Register;
