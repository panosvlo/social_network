import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import UserPosts from './UserPosts';
import api from '../services/api';
import FollowersList from './FollowersList';
import Modal from './Modal';

function UserProfile() {
  const { userId } = useParams();
  const [followers, setFollowers] = useState([]);
  const [showFollowers, setShowFollowers] = useState(false);
  const [following, setFollowing] = useState([]);
  const [showFollowing, setShowFollowing] = useState(false);

    const handleFollow = async () => {
      try {
        const token = localStorage.getItem("access_token");
        const response = await api.patch(
          `/users/${userId}/follow/`,
          {},
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        if (response.status === 200) {
          console.log(response.data.message);
        } else {
          console.error("Error following user");
        }
      } catch (error) {
        console.error(error);
      }
    };

  const handleShowFollowers = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await api.get(
        `/users/${userId}/followers/`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      if (response.status === 200) {
        setFollowers(response.data);
        setShowFollowers(true);
      } else {
        console.error("Error fetching followers");
      }
    } catch (error) {
      console.error(error);
    }
  };

    const handleShowFollowing = async () => {
      try {
        const token = localStorage.getItem("access_token");
        const response = await api.get(
          `/users/${userId}/following/`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        if (response.status === 200) {
          setFollowing(response.data);
          setShowFollowing(true);
        } else {
          console.error("Error fetching following");
        }
      } catch (error) {
        console.error(error);
      }
    };


  const handleCloseFollowers = () => {
    setShowFollowers(false);
  };

  const handleCloseFollowing = () => {
    setShowFollowing(false);
  };

  return (
    <div>
      <h2>User Profile</h2>
      <div>
        {/* Add your user avatar component here */}
      </div>
      <button onClick={handleFollow}>Follow</button>
        <button onClick={handleShowFollowers}>Show Followers</button>
        {showFollowers && (
          <Modal onClose={handleCloseFollowers}>
            <FollowersList followers={followers} handleCloseFollowers={handleCloseFollowers} title="Followers" />
          </Modal>
        )}
        <button onClick={handleShowFollowing}>Show Following</button>
        {showFollowing && (
          <Modal onClose={handleCloseFollowing}>
            <FollowersList followers={following} handleCloseFollowers={handleCloseFollowing} title="Following" />
          </Modal>
        )}
      <UserPosts userId={userId} />
    </div>
  );
}

export default UserProfile;
