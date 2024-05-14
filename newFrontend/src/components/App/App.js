import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Complaints from '../Complaints/Complaints';
import Login from '../Login/Login';
import Signup from '../Signup/Signup';
import PrivateRoute from '../PrivateRoute/PrivateRoute';
import Admin from '../Admin/Admin'
import './App.css';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userType, setUserType] = useState('user');
  const [userDetails, setUserDetails] = useState({});

  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route exact path="/" element={<Navigate to="/auth/login" />} />
        <Route exact path="/auth/login" element={<Login setIsLoggedIn={setIsLoggedIn} setSessionUserType={setUserType} setUserDetails={setUserDetails} />} />
        {/* <Route exact path="/auth/login" element={<Login setIsLoggedIn={setIsLoggedIn} setSessionUserType={setNameauth} />} /> */}
        <Route exact path="/auth/signup" element={<Signup />} />
        <Route exact path="/admin" element={<Admin />} />
        {/* Private Routes */}
        <Route path="/complaints" element={<PrivateRoute conditional={isLoggedIn} element={<Complaints userType={userType} userDetails={userDetails} />} fallback="/auth/login" />} />

        {/* Fallback Routes */}
        <Route exact path='*' element={<h1>Hello world!!</h1>} />
      </Routes>
    </Router>
  );
}

export default App;