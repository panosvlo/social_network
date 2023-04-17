import React, { useEffect, useState } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import { find as linkifyFind } from "linkifyjs"; // Import the linkify library

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
                  {/* Wrap the username in a Link component */}
                  <strong>
                    <Link to={`/profile/${post.user.id}`}>{post.user.username}</Link>
                  </strong>{" "}
                  posted:
                </p>
                <p>{renderContentWithLinks(post.content)}</p>
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