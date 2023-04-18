import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { find as linkifyFind } from "linkifyjs";
import CommentForm from "./CommentForm";
import Comment from "./Comment";
import Post from './Post';

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
    {posts.map((post) => (
      <Post key={post.id} post={post} withComments />
    ))}
  </div>
  );
}

export default UserPosts;
