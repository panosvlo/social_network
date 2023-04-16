import React from 'react';
import { useNavigate } from 'react-router-dom';
import './FollowersList.css';

const FollowersList = ({ followers, handleCloseFollowers, title }) => {
  const navigate = useNavigate();

  const handleFollowerClick = (followerId) => {
    handleCloseFollowers();
    navigate(`/profile/${followerId}`);
  };

  return (
    <div>
      <h3>{title}</h3>
      <ul>
        {followers.map((follower) => (
          <li key={follower.id} className="follower-item" onClick={() => handleFollowerClick(follower.id)}>
            {follower.username}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default FollowersList;
