import React, { useEffect, useState } from 'react';
import api from '../services/api';

const Feed = () => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSubscribedPosts();
  }, []);

  const fetchSubscribedPosts = async () => {
    try {
      const response = await api.get('/posts/');
      setPosts(response.data);
      setLoading(false);
    } catch (error) {
      console.error(error);
      setLoading(false);
    }
  };

  return (
    <div>
      <h3>Feed</h3>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <ul>
          {posts.length ? (
            posts.map((post) => <li key={post.id}>{post.content}</li>)
          ) : (
            <p>You are all caught up!</p>
          )}
        </ul>
      )}
    </div>
  );
};

export default Feed;
