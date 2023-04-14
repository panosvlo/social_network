import React from 'react';

const Feed = () => {
  // Replace this with your actual feed data
  const feedItems = ['Feed Item 1', 'Feed Item 2', 'Feed Item 3'];

  return (
    <div>
      <h3>Feed</h3>
      <ul>
        {feedItems.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </div>
  );
};

export default Feed;
