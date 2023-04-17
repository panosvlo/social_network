import React from 'react';

function TopicsList({ topics, handleCloseTopics, title }) {
  return (
    <div>
      <h2>{title}</h2>
      <ul>
        {topics.map((topic) => (
          <li key={topic.id}>{topic.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default TopicsList;
