import React from 'react';

const UserPosts = () => {
  // Replace this with your actual user posts data
  const posts = ['Post1', 'Post2', 'Post3'];

  return (
    <div>
      <h3>User Posts</h3>
      <ul>
        {posts.map((post, index) => (
          <li key={index}>{post}</li>
        ))}
      </ul>
    </div>
  );
};

export default UserPosts;
