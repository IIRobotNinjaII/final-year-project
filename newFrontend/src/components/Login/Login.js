// Login.js
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './Login.css';

const Login = ({ setIsLoggedIn, setSessionUserType }) => {
  const [userType, setUserType] = useState('user');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    try {
      e.preventDefault();

      const response = await axios.post(
        `http://localhost:8080/login/${userType}`,
        { email, password },
        { withCredentials: true }
      );

      if (response.status !== 200) {
        setError(true);
        throw Error('Login Unsuccessful!');
      }

      setError(false);
      setSessionUserType(userType);
      setIsLoggedIn(true);
      const sessionState = {
        isLoggedIn: true,
        userType: userType,
        expiry: new Date().getTime() + 6000
      }

      localStorage.setItem('sessionState', JSON.stringify(sessionState));
    } catch (error) {
      setError(true);
    }
  };

  return (
    <div className="main-login-form-container">
      <div className="login-form-container">
        <form onSubmit={handleSubmit} className="login-form">
          <h2>Login</h2>
          {error && <p className="error">Please try again!</p>}
          <div className="user-type toggle-switch">
            <input
              id="user"
              type="radio"
              value="user"
              checked={userType === 'user'}
              onChange={(e) => setUserType(e.target.value)}
              className='toggle-input'
            />
            <label className="toggle-label" htmlFor="user">
              User
            </label>
            <input
              id="officer"
              type="radio"
              value="officer"
              checked={userType === 'officer'}
              onChange={(e) => setUserType(e.target.value)}
              className='toggle-input'
            />
            <label className="toggle-label" htmlFor="officer">
              Officer
            </label>
          </div>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" onClick={handleSubmit}>
            Login
          </button>
        </form>
        <div className="signup-link">
          Don't have an account? <Link to="/auth/signup">Sign up</Link> first.
        </div>
      </div>
    </div>
  );
};

export default Login;
