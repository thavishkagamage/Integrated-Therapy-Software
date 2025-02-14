import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../login/Login.css';

const Register = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleRegister = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        
        try {
            await axios.post('http://127.0.0.1:8000/api/users/register/', {
                username,
                email,
                password,
            });
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

                <div className="register-login-link">Already have an account? <a href="/login">Login</a></div>
            </form>
        </div>
    );
};

export default Register;
