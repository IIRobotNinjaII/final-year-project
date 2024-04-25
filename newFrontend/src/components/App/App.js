import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Complaints from '../Complaints/Complaints';
import Login from '../Login/Login';
import Signup from '../Signup/Signup';
import PrivateRoute from '../PrivateRoute/PrivateRoute';
import './App.css';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userType, setUserType] = useState('user');

  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route exact path="/" element={<Navigate to="/auth/login" />} />
        <Route exact path="/auth/login" element={<Login setIsLoggedIn={setIsLoggedIn} setSessionUserType={setUserType} />} />
        <Route exact path="/auth/signup" element={<Signup />} />

        {/* Private Routes */}
        <Route path="/complaints" element={<PrivateRoute conditional={isLoggedIn} element={<Complaints userType={userType} />} fallback="/auth/login" />} />
      </Routes>
    </Router>
  );
}

export default App;