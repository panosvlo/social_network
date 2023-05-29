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
  const [page, setPage] = useState(1); // Page state
  const topicName = useTopicName(topicId);

  useEffect(() => {
    fetchPosts();
  }, [topicId, page]); // Fetch posts when topicId or page changes

  const fetchPosts = async () => {
    try {
      const response = await api.get(`/topics/${topicId}/posts/?page=${page}`);
      if (page > 1) {
        setPosts(prevPosts => [...prevPosts, ...response.data.results]);
      } else {
        setPosts(response.data.results);
      }
    } catch (error) {
      console.error('Error fetching posts:', error);
    }
  };

  const handleLoadMore = () => {
    setPage(prevPage => prevPage + 1);
  };

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
      {posts.length ? (
        posts.map((post) => (
          <Post key={post.id} post={post} withComments={true} />
        ))
      ) : (
        <p>No posts yet.</p>
      )}
      <button onClick={handleLoadMore}>Load More</button>
    </div>
  );
};

export default TopicPage;
