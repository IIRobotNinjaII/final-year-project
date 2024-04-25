// Login.js
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Login.css';

const Login = ({ setIsLoggedIn, setSessionUserType }) => {
  const [userType, setUserType] = useState('user');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {

      const response = await axios.post(
        `http://localhost:8080/login/${userType}`,
        { email, password },
        { withCredentials: true }
      );

      if (response.status !== 200) {
        throw Error();
      } else {
        setIsLoggedIn(true);
        setSessionUserType(userType);
        navigate('/complaints');
      }
    } catch (error) {
      setError(true);
    }
  };

  const handleUserTypeChange = (e) => {
    setUserType(e.target.value);
  }

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
              onChange={handleUserTypeChange}
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
              onChange={handleUserTypeChange}
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
          <button type="submit">
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
