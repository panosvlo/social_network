import React from 'react';

const Comment = ({ comment }) => {
  return (
    <div style={{ marginLeft: "1rem" }}>
      <p>
        <strong>{comment.user.username}:</strong> {comment.content}
      </p>
    </div>
  );
};

export default Comment;
