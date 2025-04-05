import React, { useEffect } from 'react'
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useState } from 'react';
import './Profile.css';

const Profile = ({handleLogout}) => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [firstName, setFirstName] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const userResponse = await axios.get('http://127.0.0.1:8000/api/users/userinfo/', {
                    headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` }
                });
                console.log('Fetched user data:', userResponse.data); // For debugging purposes
                setUsername(userResponse.data.username || 'Error fetching username!');
                setFirstName(userResponse.data.first_name || 'Error fetching first name!');
                setEmail(userResponse.data.email || 'Error fetching email!');
            } catch (error) {
                console.error('Error fetching user data:', error);
            }
        };
        fetchUserData();
    }, []);

    const logout = () => {
        setLoading(true);
        try {
            handleLogout();
            alert('Logout successful!');
            navigate('/');
        } catch (error) {
            console.error('Logout failed:', error);
            alert('An error occurred while logging out. Please try again.');
        } finally {
            setLoading(false);
        }
    }


    return (
        <div className="profile-container">
            <div className="profile-card">
                <h2>Profile Info</h2>
                <div className="profile-info">
                    <p><strong>First Name:</strong> {firstName}</p>
                    <p><strong>Username:</strong> {username}</p>
                    <p><strong>Email:</strong> {email}</p>
                </div>
                <button disabled={loading} className="logout-button" onClick={logout}>
                    {loading ? 'Logging out...' : 'Logout'}
                </button>
            </div>
        </div>
    )
}

export default Profile
