// UserPosts.js

import React, { useState, useEffect } from 'react';
import api from '../services/api';

function UserPosts({ userId }) {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    async function fetchUserPosts() {
      try {
        const response = await api.get(`/users/${userId}/posts/`);
        setPosts(response.data);
      } catch (error) {
        console.error('Error fetching user posts:', error);
      }
    }
    if (userId) {
      fetchUserPosts();
    }
  }, [userId]);

  return (
    <div>
      <h3>User Posts</h3>
      <ul>
        {posts.map((post) => (
          <li key={post.id}>{post.content}</li>
        ))}
      </ul>
    </div>
  );
}

export default UserPosts;
