import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Post from './Post';
import api from '../services/api';
import SignOutLink from './SignOutLink';
import { Link } from 'react-router-dom';
import useTopicName from './useTopicName';
import jwt_decode from 'jwt-decode';

const TopicPage = () => {
  const { topicId } = useParams();
  const [posts, setPosts] = useState([]);
  const topicName = useTopicName(topicId);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await api.get(`/topics/${topicId}/posts/`);
        setPosts(response.data);
      } catch (error) {
        console.error('Error fetching posts:', error);
      }
    };

    fetchPosts();
  }, [topicId]);

  const [currentUserId, setCurrentUserId] = useState(null);

  useEffect(() => {
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
    <div>
      <div>
        <Link to={`/`}>Go to Home Page</Link>
        <div style={{ marginTop: '8px' }}>
          {currentUserId && <Link to={`/profile/${currentUserId}`}>Go to User Profile</Link>}
        </div>
        <div style={{ marginTop: '8px' }}>
          <SignOutLink to="/">Sign Out</SignOutLink>
        </div>
      </div>
      <h2>Posts for Topic #{topicName}</h2>
      {posts.map((post) => (
        <Post key={post.id} post={post} withComments={true} />
      ))}
    </div>
  );
};

export default TopicPage;
