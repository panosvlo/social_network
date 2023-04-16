import React from 'react';
import { useParams } from 'react-router-dom';
import UserPosts from './UserPosts';
import Followers from './Followers';

function UserProfile() {
  const { userId } = useParams();

  return (
    <div>
      <h2>User Profile</h2>
      <div>
        {/* Add your user avatar component here */}
      </div>
      <UserPosts userId={userId} />
      <Followers />
    </div>
  );
}

export default UserProfile;
