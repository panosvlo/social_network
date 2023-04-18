import React, { useEffect, useState } from "react";
import { Link } from 'react-router-dom';
import CommentForm from './CommentForm';
import Comment from './Comment';
import { find as linkifyFind } from "linkifyjs";
import api from "../services/api";

const Post = ({ post, withComments }) => {
  const [posts, setPosts] = useState([]);
  const [topicName, setTopicName] = useState('');

  useEffect(() => {
    const fetchTopicName = async () => {
      try {
        const response = await api.get(`/topics/${post.topic}/`);
        setTopicName(response.data.name);
      } catch (error) {
        console.error('Error fetching topic name:', error);
      }
    };

    fetchTopicName();
  }, [post.topic]);
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

  const handleLike = async (postId) => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await api.post(`/posts/${postId}/like/`, {}, {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (response.status === 200) {
        // Update the post's like count in the state
        setPosts(
          posts.map((post) =>
            post.id === postId ? { ...post, like_count: post.like_count + 1 } : post
          )
        );
      } else {
        console.error("Error liking the post");
      }
    } catch (error) {
      console.error("Error liking the post:", error);
    }
  };

  const formatHref = (href, type) => {
    if (type === "url" && !/^https?:\/\//.test(href)) {
      return `http://${href}`;
    }
    return href;
  };

  return (
    <div style={{ border: '1px solid #ccc', padding: '1rem', marginBottom: '1rem' }}>
      <p>
        <strong>
          <Link to={`/profile/${post.user.id}`}>{post.user.username}</Link>
        </strong>{' '}
        posted on {new Date(post.created_at).toLocaleDateString()}:
      </p>
      <p>
        <span style={{ fontWeight: 'bold' }}>#{topicName}</span>
      </p>
      <p>{renderContentWithLinks(post.content)}</p>
      <p>
        <strong>Likes:</strong> {post.like_count} <strong>Comments:</strong> {post.comments_count}
      </p>
      <button onClick={() => handleLike(post.id)}>Like</button>
      {withComments && (
        <>
          <CommentForm
            postId={post.id}
            onCommentSubmit={(newComment) => {
              // Update the post's comments count in the parent component
            }}
          />
          {post.comments.map((comment) => (
            <Comment key={comment.id} comment={comment} />
          ))}
        </>
      )}
    </div>
  );
};

export default Post;
