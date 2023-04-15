
import React, { useState, useEffect } from "react";
import api from "../services/api";

const TopicSubscription = () => {
  const [topics, setTopics] = useState([]);
  const [selectedTopic, setSelectedTopic] = useState("");

  useEffect(() => {
    const fetchTopics = async () => {
      try {
        const response = await api.get("/topics/");
        setTopics(response.data);
      } catch (error) {
        console.error("Error fetching topics:", error);
      }
    };

    fetchTopics();
  }, []);

  const handleSubscribe = async () => {
    if (!selectedTopic) {
      alert("Please select a topic.");
      return;
    }

    try {
      const token = localStorage.getItem("access_token");
      console.log("Access token for topics:", token);
      const response = await api.patch(
        "/subscribe/",
        { topic_name: selectedTopic },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      if (response.status === 200) {
        alert(`Subscribed to ${selectedTopic}`);
      } else {
        console.error("Error subscribing to topic");
      }
    } catch (error) {
      console.error("Error subscribing to topic:", error);
    }
  };

  return (
    <div>
      <h3>Subscribe to a topic</h3>
      <select
        value={selectedTopic}
        onChange={(e) => setSelectedTopic(e.target.value)}
      >
        <option value="">Select a topic</option>
        {topics.map((topic) => (
          <option key={topic.id} value={topic.name}>
            {topic.name}
          </option>
        ))}
      </select>
      <button onClick={handleSubscribe}>Subscribe</button>
    </div>
  );
};

export default TopicSubscription;