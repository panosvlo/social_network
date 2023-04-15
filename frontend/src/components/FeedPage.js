import React from 'react';
import Avatar from './Avatar';
import Followers from './Followers';
import UserPosts from './UserPosts';
import CreatePost from './CreatePost';
import Feed from './Feed';
import TopicSubscription from "./TopicSubscription";

const FeedPage = () => {
  return (
    <div style={{ display: 'flex' }}>
      <div style={{ flex: 1 }}>
        <Avatar />
        <Followers />
        <UserPosts />
        <CreatePost />
        <TopicSubscription />
      </div>
      <div style={{ flex: 1 }}>
        <Feed />
      </div>
    </div>
  );
};

export default FeedPage;
