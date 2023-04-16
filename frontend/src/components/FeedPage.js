import React, { useEffect, useState } from 'react';
import Avatar from './Avatar';
import Followers from './Followers';
import UserPosts from './UserPosts';
import CreatePost from './CreatePost';
import Feed from './Feed';
import TopicSubscription from "./TopicSubscription";
import { Link } from 'react-router-dom';
import jwt_decode from 'jwt-decode';


const FeedPage = () => {
  const [currentUserId, setCurrentUserId] = useState(null);

  useEffect(() => {
    // Get the access token from your authentication system
    const accessToken = localStorage.getItem('access_token');

    if (accessToken) {
      try {
        const decodedToken = jwt_decode(accessToken);
        setCurrentUserId(decodedToken.user_id);
        console.log("Current User ID:", decodedToken.user_id);
      } catch (error) {
        console.error('Error decoding JWT:', error);
      }
    }
  }, []);
  return (
    <div style={{ display: 'flex' }}>
      <div style={{ flex: 1 }}>
        <Avatar />
        {currentUserId && <Link to={`/profile/${currentUserId}`}>Go to User Profile</Link>}
        <Followers />
        <UserPosts />
        <CreatePost />
        <TopicSubscription />
      </div>
      <div style={{ flex: 1 }}>
        <Feed />
      </div>
    </div>
  );
};

export default FeedPage;
