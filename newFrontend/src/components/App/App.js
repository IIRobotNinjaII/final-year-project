import React, { useState, useEffect } from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from 'react-router-dom'; // Import Navigate
import Complaints from '../Complaints/Complaints';
import Login from '../Login/Login';
import Signup from '../Signup/Signup';
import './App.css';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userType, setUserType] = useState('user');
  const [signupSuccess, setSignupSuccess] = useState(false);

  useEffect(() => {
    const sessionState = JSON.parse(localStorage.getItem('sessionState'));
    if(sessionState) {

      setIsLoggedIn(sessionState.isLoggedIn);
      setUserType(sessionState.userType);
    }
  }, []);

  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<Navigate to="/auth/login" />} />
        <Route
          exact
          path="/auth/login"
          element={
            isLoggedIn ? (
              <Navigate to="/complaints" />
            ) : (
              <Login
                setIsLoggedIn={setIsLoggedIn}
                setSessionUserType={setUserType}
              />
            )
          }
        />
        <Route
          exact
          path="/complaints"
          element={
            isLoggedIn ? (
              <Complaints />
            ) : (
              <Navigate to="/auth/login" userType={userType} />
            )
          }
        />
        <Route
          exact
          path="/auth/signup"
          element={
            signupSuccess ? (
              <Login
                setIsLoggedIn={setIsLoggedIn}
                setSessionUserType={setUserType}
              />
            ) : (
              <Signup setSignupSuccess={setSignupSuccess} />
            )
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
