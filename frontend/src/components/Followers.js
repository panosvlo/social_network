import React from 'react';

const Followers = () => {
  // Replace this with your actual followers data
  const followers = ['Follower1', 'Follower2', 'Follower3'];

  return (
    <div>
      <h3>Followers</h3>
      <ul>
        {followers.map((follower, index) => (
          <li key={index}>{follower}</li>
        ))}
      </ul>
    </div>
  );
};

export default Followers;
