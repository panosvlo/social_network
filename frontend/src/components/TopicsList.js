import React from 'react';

function TopicsList({ topics, handleCloseTopics, title, onUnsubscribe }) {
  const handleUnsubscribe = (topicId) => {
    onUnsubscribe(topicId);
  };

  return (
    <div>
      <h2>{title}</h2>
      <ul>
        {topics.map((topic) => (
          <li key={topic.id}>
            {topic.name}
            <button onClick={() => handleUnsubscribe(topic.id)}>Unsubscribe</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TopicsList;
