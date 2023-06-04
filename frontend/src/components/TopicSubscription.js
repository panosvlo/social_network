import React, { useState, useEffect } from "react";
import api from "../services/api";
import Autosuggest from "react-autosuggest";
import "./TopicSubscription.css";

const TopicSubscription = () => {
  const [topics, setTopics] = useState([]);
  const [selectedTopic, setSelectedTopic] = useState("");
  const [suggestions, setSuggestions] = useState([]);

  useEffect(() => {
    const fetchTopics = async () => {
      try {
        const response = await api.get('/topics/');
        if(Array.isArray(response.data.results)) {
          setTopics(response.data.results);
        } else {
          console.error('Received data is not an array:', response.data.results);
          setTopics([]);
        }
      } catch (error) {
        console.error('Error fetching topics:', error);
      }
    };

    fetchTopics();
  }, []);


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

  const onSuggestionsFetchRequested = ({ value }) => {
    setSuggestions(getSuggestions(value));
  };

  const onSuggestionsClearRequested = () => {
    setSuggestions([]);
  };

  const getSuggestionValue = (suggestion) => suggestion.name;

  const renderSuggestion = (suggestion) => <div>{suggestion.name}</div>;

  const inputProps = {
    placeholder: "Select a topic",
    value: selectedTopic,
    onChange: (_, { newValue }) => {
      setSelectedTopic(newValue);
    },
  };

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
      <Autosuggest
        suggestions={suggestions}
        onSuggestionsFetchRequested={onSuggestionsFetchRequested}
        onSuggestionsClearRequested={onSuggestionsClearRequested}
        getSuggestionValue={getSuggestionValue}
        renderSuggestion={renderSuggestion}
        inputProps={inputProps}
      />
      <button onClick={handleSubscribe}>Subscribe</button>
    </div>
  );
};

export default TopicSubscription;
