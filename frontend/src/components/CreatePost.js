import React, { useState } from "react";
import api from "../services/api";

const CreatePost = () => {
  const [content, setContent] = useState("");
  const [topic, setTopic] = useState("");

  const handleCreatePost = async () => {
    try {
      const token = localStorage.getItem("access_token");
      console.log("Access token:", token);
      const response = await api.post(
        "/posts/",
        { content: content, topic_name: topic },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      if (response.status === 201) {
        setContent("");
        setTopic("");
        // Refresh the feed or update the state to display the new post
      } else {
        console.error("Error creating post");
      }
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h3>Create a new post</h3>
      <label>
        Topic:
        <input
          type="text"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          placeholder="Topic..."
        />
      </label>
      <br />
      <textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="Write your post..."
      ></textarea>
      <button onClick={handleCreatePost}>Post</button>
    </div>
  );
};

export default CreatePost;
