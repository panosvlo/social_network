import React from 'react';

const CreatePost = ({ postContent, onPostContentChange, onCreatePost }) => {
  return (
    <div>
      <h3>Create a new post</h3>
      <textarea
      value={postContent}
      onChange={(e) => onPostContentChange(e.target.value)}
      placeholder="Write your post..."
      />
      <button onClick={onCreatePost}>Post</button>
    </div>
  );
};

export default CreatePost;
