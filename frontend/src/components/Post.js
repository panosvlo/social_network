import React, { useEffect, useState } from "react";
import { Link } from 'react-router-dom';
import CommentForm from './CommentForm';
import Comment from './Comment';
import { find as linkifyFind } from "linkifyjs";
import api from "../services/api";
import jwt_decode from "jwt-decode";
import useTopicName from './useTopicName';

const Post = ({ post, withComments }) => {
  const topicName = useTopicName(post.topic);
  const [likeCount, setLikeCount] = useState(post.like_count);
  const [liked, setLiked] = useState(false);
  const [currentUserId, setCurrentUserId] = useState(null);

  useEffect(() => {
    fetchCurrentUserId();
  }, [post.topic]);

  useEffect(() => {
    if (currentUserId !== null) {
      checkIfUserLikedPost();
    }
  }, [currentUserId]);

  const fetchCurrentUserId = () => {
    const accessToken = localStorage.getItem("access_token");
    if (accessToken) {
      try {
        const decodedToken = jwt_decode(accessToken);
        setCurrentUserId(decodedToken.user_id);
      } catch (error) {
        console.error("Error decoding JWT:", error);
      }
    }
  };

  const checkIfUserLikedPost = () => {
    if (post.likes && post.likes.includes(currentUserId)) {
      setLiked(true);
    } else {
      setLiked(false);
    }
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

  const handleLike = async (postId) => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await api.post(`/posts/${postId}/like/`, {}, {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (response.status === 200) {
        // Update the like count and the 'liked' state based on the current state
        if (liked) {
          setLikeCount(likeCount - 1);
        } else {
          setLikeCount(likeCount + 1);
        }
        setLiked(!liked);
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
        <span style={{ fontWeight: 'bold' }}>
          <Link to={`/topics/${post.topic}`}>#{topicName}</Link>
        </span>
      </p>
      <p>{renderContentWithLinks(post.content)}</p>
      <p>
        <strong>Likes:</strong> {likeCount} <strong>Comments:</strong> {post.comments_count}
      </p>
      <button onClick={() => handleLike(post.id)}>{liked ? "Unlike" : "Like"}</button>
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
