import React, { useState, useEffect } from "react";
import api from "../services/api";
import './TopicSubscription.css';

const CreatePost = () => {
  const [content, setContent] = useState("");
  const [topic, setTopic] = useState("");
  const [suggestedTopics, setSuggestedTopics] = useState([]);
  const [topics, setTopics] = useState([]);

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

  useEffect(() => {
    const fetchTopics = async () => {
      try {
        const response = await api.get('/topics/');
        setTopics(response.data);
      } catch (error) {
        console.error('Error fetching topics:', error);
      }
    };

    fetchTopics();
  }, []);

  const handleTopicChange = (e) => {
    const inputTopic = e.target.value;
    setTopic(inputTopic);

    if (inputTopic) {
      setSuggestedTopics(
        topics.filter((topic) =>
          topic.name.toLowerCase().startsWith(inputTopic.toLowerCase())
        )
      );
    } else {
      setSuggestedTopics([]);
    }
  };

  const selectSuggestedTopic = (topicName) => {
    setTopic(topicName);
    setSuggestedTopics([]);
  };

  return (
    <div>
      <h3>Create a new post</h3>
      <label>
        Topic:
        <input
          type="text"
          value={topic}
          onChange={handleTopicChange}
          placeholder="Topic..."
        />
      </label>
      <div className="suggested-topics">
        {suggestedTopics.map((suggestedTopic) => (
          <div
            key={suggestedTopic.id}
            className="suggested-topic"
            onClick={() => selectSuggestedTopic(suggestedTopic.name)}
          >
            {suggestedTopic.name}
          </div>
        ))}
      </div>
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