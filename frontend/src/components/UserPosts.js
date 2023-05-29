import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { find as linkifyFind } from "linkifyjs";
import CommentForm from "./CommentForm";
import Comment from "./Comment";
import Post from './Post';

function UserPosts({ userId }) {
  const [posts, setPosts] = useState([]);
  const [page, setPage] = useState(1);

  useEffect(() => {
    fetchUserPosts();
  }, [userId, page]);

  const fetchUserPosts = async () => {
    try {
      const response = await api.get(`/users/${userId}/posts/?page=${page}`);
      if (page > 1) {
        setPosts(prevPosts => [...prevPosts, ...response.data.results]);
      } else {
        setPosts(response.data.results);
      }
    } catch (error) {
      console.error('Error fetching user posts:', error);
    }
  };

  const handleLoadMore = () => {
    setPage(prevPage => prevPage + 1);
  };

  return (
    <div>
      <h3>User Posts</h3>
      {posts.length ? (
        posts.map((post) => (
          <Post key={post.id} post={post} withComments />
        ))
      ) : (
        <p>No posts yet.</p>
      )}
      <button onClick={handleLoadMore}>Load More</button>
    </div>
  );
}

export default UserPosts;
