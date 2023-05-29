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
  const [page, setPage] = useState(1);  // Add a state for current page number
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
      const response = await api.get(`/posts/?page=${page}&with_comments=true`);
      // If this is not the first page, we want to append posts instead of replacing them
      if (page > 1) {
        setPosts(prevPosts => [...prevPosts, ...response.data.results]);
      } else {
        setPosts(response.data.results);
      }
      setLoading(false);
    } catch (error) {
      console.error(error);
      setLoading(false);
    }
  };

  const handleLoadMore = () => {
    setPage(prevPage => prevPage + 1);
  };

  // Call fetchSubscribedPosts whenever the page number changes
  useEffect(() => {
    fetchSubscribedPosts();
  }, [page]);

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
        <button onClick={handleLoadMore}>Load More</button>
      </div>
    )}
  </div>
  );
};

export default Feed;