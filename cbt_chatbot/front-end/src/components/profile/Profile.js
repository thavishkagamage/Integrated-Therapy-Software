import React, { useEffect } from 'react'
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useState } from 'react';
import './Profile.css';

const Profile = ({handleLogout, handleDeleteProfile}) => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [firstName, setFirstName] = useState('');
    const [loggingOut, setLoggingOut] = useState(false);
    const [deleting, setDeleting] = useState(false); // State to manage deletion loading state
    const navigate = useNavigate();

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const accesToken = localStorage.getItem('accessToken') // Ensure the token exists before making the request
                const userResponse = await axios.get('http://127.0.0.1:8000/api/users/userinfo/', {
                    headers: { Authorization: `Bearer ${accesToken}` }
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
        setLoggingOut(true);
        try {
            handleLogout();
            alert('Logout successful!');
            navigate('/');
        } catch (error) {
            console.error('Logout failed:', error);
            alert('An error occurred while logging out. Please try again.');
        } finally {
            setLoggingOut(false);
        }
    }

    const deleteProfile = () => {
        setDeleting(true);
        try {
            const confirmed = window.confirm("Are you sure you want to delete your profile? This action cannot be undone.");
            if (!confirmed) {
                return;
            }  
            handleDeleteProfile();
            alert('Profile deleted!');
            navigate('/');
        } catch (error) {
            console.error('Deletion failed:', error);
            alert('An error occurred while deleting profile. Please try again.');
        } finally {
            setDeleting(false);
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
                <button disabled={loggingOut} className="logout-button" onClick={logout}>
                    {loggingOut ? 'Logging out...' : 'Logout'}
                </button>
                <button disabled={deleting} className="logout-button" onClick={deleteProfile}>
                    {deleting ? 'Deleting...' : 'Delete Profile'}
                </button>
            </div>
        </div>
    )
}

export default Profile
