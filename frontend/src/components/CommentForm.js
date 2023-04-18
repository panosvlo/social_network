import React, { useState } from "react";
import api from "../services/api";

function CommentForm({ postId, onCommentSubmit }) {
  const [comment, setComment] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const token = localStorage.getItem("access_token");
      const response = await api.post(`/posts/${postId}/comment/`, { content: comment }, {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (response.status === 201) {
        setComment("");
        onCommentSubmit(response.data);
      } else {
        console.error("Error submitting the comment");
      }
    } catch (error) {
      console.error("Error submitting the comment:", error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={comment}
        onChange={(e) => setComment(e.target.value)}
        placeholder="Write a comment..."
      />
      <button type="submit">Comment</button>
    </form>
  );
}

export default CommentForm;