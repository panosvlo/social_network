import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { find as linkifyFind } from 'linkifyjs'; // Import the linkify library

function UserPosts({ userId }) {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    async function fetchUserPosts() {
      try {
        const response = await api.get(`/users/${userId}/posts/`);
        setPosts(response.data);
      } catch (error) {
        console.error('Error fetching user posts:', error);
      }
    }
    if (userId) {
      fetchUserPosts();
    }
  }, [userId]);

  const formatHref = (href, type) => {
    if (type === "url" && !/^https?:\/\//.test(href)) {
      return `http://${href}`;
    }
    return href;
  };

  const renderContentWithLinks = (content) => {
    const links = linkifyFind(content);
    let lastIndex = 0;
    const elements = [];

    links.forEach((link, index) => {
      elements.push(content.slice(lastIndex, link.start));
      elements.push(
        <a href={formatHref(link.href, link.type)} key={index} target="_blank" rel="noopener noreferrer">
          {link.value}
        </a>
      );
      lastIndex = link.end;
    });

    elements.push(content.slice(lastIndex));

    return elements;
  };

  return (
    <div>
    <h3>User Posts</h3>
    {posts.map((post) => (
      <div key={post.id} style={{ border: "1px solid #ccc", padding: "1rem", marginBottom: "1rem" }}>
        <p>Posted on {new Date(post.created_at).toLocaleDateString()}:</p>
        <p>{renderContentWithLinks(post.content)}</p>
      </div>
    ))}
  </div>
  );
}

export default UserPosts;
