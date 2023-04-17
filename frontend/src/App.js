import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import RegisterForm from './components/RegisterForm';
import SignInForm from './components/SignInForm';
import Feed from './components/Feed';
import FeedPage from './components/FeedPage';
import UserProfile from './components/UserProfile';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<FeedPage />} />
        <Route path="/signin" element={<SignInForm />} />
        <Route path="/register" element={<RegisterForm />} />
        <Route path="/feed" element={<FeedPage />} />
        <Route path="/profile/:userId" element={<UserProfile />} />
      </Routes>
    </Router>
  );
}

export default App;
