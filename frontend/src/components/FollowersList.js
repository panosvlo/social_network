import React from 'react';
import { Link } from 'react-router-dom';

const FollowersList = ({ followers }) => {
  return (
    <div>
      <h3>Followers</h3>
      <ul>
        {followers.map((follower) => (
          <li key={follower.id}>
            <Link to={`/profile/${follower.id}`}>{follower.username}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default FollowersList;
