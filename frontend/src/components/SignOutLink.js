import React from 'react';
import { Link } from 'react-router-dom';

const SignOutLink = ({ children, ...props }) => {
  const handleSignOut = (event) => {
    event.preventDefault();
    localStorage.removeItem('access_token');
    window.location.reload();
  };

  return (
    <Link {...props} onClick={handleSignOut}>
      {children}
    </Link>
  );
};

export default SignOutLink;
