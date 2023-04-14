import React, { useState } from 'react';
import Avatar from './Avatar';
import Followers from './Followers';
import UserPosts from './UserPosts';
import CreatePost from './CreatePost';
import Feed from './Feed';
import api from '../services/api';

const FeedPage = () => {
  const [postContent, setPostContent] = useState('');

  const handleCreatePost = async () => {
    try {
      const token = localStorage.getItem('access_token');
      console.log("Access token:", token);
      const response = await api.post(
        '/posts/',
        { content: postContent },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      if (response.status === 201) {
        setPostContent('');
        // Refresh the feed or update the state to display the new post
      } else {
        console.error('Error creating post');
      }
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div style={{ display: 'flex' }}>
      <div style={{ flex: 1 }}>
        <Avatar />
        <Followers />
        <UserPosts />
        <CreatePost
          postContent={postContent}
          onPostContentChange={setPostContent}
          onCreatePost={handleCreatePost}
        />
      </div>
      <div style={{ flex: 1 }}>
        <Feed />
      </div>
    </div>
  );
};

export default FeedPage;
