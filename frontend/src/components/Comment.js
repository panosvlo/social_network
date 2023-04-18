import React from 'react';
import { Link } from 'react-router-dom';
import './Comment.css';

const Comment = ({ comment }) => {
  return (
    <div className="comment-container">
      <div className="comment-user">
        <Link to={`/profile/${comment.user}`} className="comment-username">
          {comment.username}
        </Link>
        {' '} - Posted at {new Date(comment.created_at).toLocaleDateString()}
      </div>
      <div className="comment-content">{comment.content}</div>
    </div>
  );
};

export default Comment;
