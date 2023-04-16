import React from 'react';
import { useParams } from 'react-router-dom';
import UserPosts from './UserPosts';
import Followers from './Followers';
import api from '../services/api';

function UserProfile() {
  const { userId } = useParams();

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

  return (
    <div>
      <h2>User Profile</h2>
      <div>
        {/* Add your user avatar component here */}
      </div>
      <button onClick={handleFollow}>Follow</button>
      <UserPosts userId={userId} />
      <Followers />
    </div>
  );
}

export default UserProfile;
