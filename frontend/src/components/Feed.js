import React, { useEffect, useState } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import { find as linkifyFind } from "linkifyjs";
import CommentForm from "./CommentForm";
import Comment from "./Comment";
import Post from './Post';

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
      const response = await api.get("/posts/?with_comments=true");
      setPosts(response.data);
      setLoading(false);
    } catch (error) {
      console.error(error);
      setLoading(false);
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
            <Post key={post.id} post={post} withComments />
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