import React, { useEffect, useState } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import { find as linkifyFind } from "linkifyjs";
import CommentForm from "./CommentForm";

const Feed = () => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const checkAuthentication = async () => {
      const token = localStorage.getItem("access_token");
      console.log("Access token:", token);
      if (!token) {
        navigate("/signin");
      } else {
        fetchSubscribedPosts();
      }
    };

    checkAuthentication();
  }, []);

  const fetchSubscribedPosts = async () => {
    try {
      const response = await api.get("/posts/");
      setPosts(response.data);
      setLoading(false);
    } catch (error) {
      console.error(error);
      setLoading(false);
    }
  };

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

return (
  <div>
    <h3>Feed</h3>
    {loading ? (
      <p>Loading...</p>
    ) : (
      <div>
        {posts.length ? (
          posts.map((post) => (
            <div key={post.id} style={{ border: "1px solid #ccc", padding: "1rem", marginBottom: "1rem" }}>
              <p>
                <strong>
                  <Link to={`/profile/${post.user.id}`}>{post.user.username}</Link>
                </strong>{" "}
                posted on {new Date(post.created_at).toLocaleDateString()}:
              </p>
              <p>{renderContentWithLinks(post.content)}</p>
              <p>
                <strong>Likes:</strong> {post.like_count}{" "}
                <strong>Comments:</strong> {post.comments_count}
              </p>
              <button onClick={() => handleLike(post.id)}>Like</button>
              <CommentForm
                postId={post.id}
                onCommentSubmit={(newComment) => {
                  setPosts(
                    posts.map((p) =>
                      p.id === post.id
                        ? { ...p, comments_count: p.comments_count + 1 }
                        : p
                    )
                  );
                }}
              />
            </div>
          ))
        ) : (
          <p>You are all caught up!</p>
        )}
      </div>
    )}
  </div>
  );
};

export default Feed;