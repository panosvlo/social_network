import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import UserPosts from './UserPosts';
import api from '../services/api';
import FollowersList from './FollowersList';
import TopicsList from './TopicsList';
import Modal from './Modal';

function UserProfile() {
  const { userId } = useParams();
  const [followers, setFollowers] = useState([]);
  const [showFollowers, setShowFollowers] = useState(false);
  const [following, setFollowing] = useState([]);
  const [showFollowing, setShowFollowing] = useState(false);
  const [isFollowing, setIsFollowing] = useState(false);
  const [topics, setTopics] = useState([]);
  const [showTopics, setShowTopics] = useState(false);

  useEffect(() => {
    checkIsFollowing();
  }, [userId]);

  const checkIsFollowing = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await api.get(`/users/${userId}/is_following/`, {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.status === 200) {
        setIsFollowing(response.data.is_following);
      }
    } catch (error) {
      console.error("Error checking follow status:", error);
    }
  };

  const handleFollow = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const endpoint = isFollowing ? "/unfollow/" : "/follow/";
      const response = await api.patch(
        `/users/${userId}${endpoint}`,
        {},
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      if (response.status === 200) {
        console.log(response.data.message);
        setIsFollowing(!isFollowing); // Add this line to update the isFollowing state
      } else {
        console.error("Error following/unfollowing user");
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

  const handleShowTopics = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await api.get(
        `/users/${userId}/topics/`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      if (response.status === 200) {
        setTopics(response.data);
        setShowTopics(true);
      } else {
        console.error("Error fetching topics");
      }
    } catch (error) {
      console.error(error);
    }
  };

  const handleUnsubscribe = async (topicId) => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await api.patch(
        `/users/${userId}/topics/${topicId}/unsubscribe/`,
        {},
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      if (response.status === 200) {
        console.log(response.data.message);
        setTopics(topics.filter((topic) => topic.id !== topicId));
      } else {
        console.error("Error unsubscribing from topic");
      }
    } catch (error) {
      console.error(error);
    }
  };

  const handleCloseTopics = () => {
    setShowTopics(false);
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
      <button onClick={handleFollow}>{isFollowing ? 'Unfollow' : 'Follow'}</button>
      <button onClick={handleShowFollowers}>Followers</button>
      {showFollowers && (
        <Modal onClose={handleCloseFollowers}>
          <FollowersList followers={followers} handleCloseFollowers={handleCloseFollowers} title="Followers" />
        </Modal>
      )}
      <button onClick={handleShowFollowing}>Following</button>
      {showFollowing && (
        <Modal onClose={handleCloseFollowing}>
          <FollowersList followers={following} handleCloseFollowers={handleCloseFollowing} title="Following" />
        </Modal>
        )}
      <button onClick={handleShowTopics}>Followed Topics</button>
      {showTopics && (
        <Modal onClose={handleCloseTopics}>
          <TopicsList
            topics={topics}
            handleCloseTopics={handleCloseTopics}
            title="Topics"
            onUnsubscribe={handleUnsubscribe} // Pass the handleUnsubscribe function as a prop
          />
        </Modal>
      )}
      <UserPosts userId={userId} />
    </div>
  );
}

export default UserProfile;
