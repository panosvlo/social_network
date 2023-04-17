import React, { useState, useEffect } from "react";
import api from "../services/api";
import Autosuggest from "react-autosuggest";
import "./TopicSubscription.css";
import "./CreatePost.css";

const CreatePost = () => {
  const [content, setContent] = useState("");
  const [topic, setTopic] = useState("");
  const [suggestedTopics, setSuggestedTopics] = useState([]);
  const [topics, setTopics] = useState([]);
  const [suggestions, setSuggestions] = useState([]);

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

  const handleTopicChange = (_, { newValue }) => {
    setTopic(newValue);
  };

  const getSuggestions = (value) => {
    const inputValue = value.trim().toLowerCase();
    const inputLength = inputValue.length;

    return inputLength === 0
      ? []
      : topics.filter(
          (topic) =>
            topic.name.toLowerCase().slice(0, inputLength) === inputValue
        );
  };



  const inputProps = {
    placeholder: "Select a topic",
    value: topic,
    onChange: handleTopicChange,
  };

  const selectSuggestedTopic = (topicName) => {
    setTopic(topicName);
    setSuggestedTopics([]);
  };

    const onSuggestionsFetchRequested = ({ value }) => {
      setSuggestions(getSuggestions(value));
    };

    const onSuggestionsClearRequested = () => {
      setSuggestions([]);
    };

    const getSuggestionValue = (suggestion) => suggestion.name;

    const renderSuggestion = (suggestion) => <div>{suggestion.name}</div>;

  return (
    <div>
      <h3>Create a new post</h3>
      <label>
        <Autosuggest
          suggestions={suggestions}
          onSuggestionsFetchRequested={onSuggestionsFetchRequested}
          onSuggestionsClearRequested={onSuggestionsClearRequested}
          getSuggestionValue={getSuggestionValue}
          renderSuggestion={renderSuggestion}
          inputProps={inputProps}
        />
      </label>
      {/* Remove the suggested-topics div */}
      <br />
      <textarea
        className="create-post-textarea"
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="Write your post..."
      ></textarea>
      <br />
      <button onClick={handleCreatePost}>Post</button>
    </div>
  );
};

export default CreatePost;