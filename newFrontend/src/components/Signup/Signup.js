// Sign-Up.js
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './Signup.css';

const Signup = ({ setSignupSuccess }) => {
  const [userType, setUserType] = useState('user');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {

    try {
      e.preventDefault();
      
      const url = `http://localhost:8080/signup/${userType}`;
      const body = {
        name: name,
        email: email,
        password: password
      };

      const response = await axios.post(url, body);
      
      if(response.status !== 201) { 
        throw Error('Could not signup');
      }

      setError(false);
      setSignupSuccess(true);

    } catch(error) {
      setError(true);
    }
  };

  return (
    <div className="main-signup-form-container">
      <div className="signup-form-container">
        <form onSubmit={handleSubmit} className="signup-form">
          <h2>Sign-Up</h2>
          {error &&<p className='error'>Please try again!</p>}
          <div className="user-type">
            <input
              id="user"
              type="radio"
              value="user"
              checked={userType === 'user'}
              onChange={(e) => setUserType(e.target.value)}
            />
            <label className="user" htmlFor="user">
              User
            </label>
            <input
              id="officer"
              type="radio"
              value="officer"
              checked={userType === 'officer'}
              onChange={(e) => setUserType(e.target.value)}
            />
            <label className="officer" htmlFor="officer">
              Officer
            </label>
          </div>
          <div className="form-group">
            <label id="name">Name</label>
            <input
              htmlFor="name"
              type="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label id="email">Email</label>
            <input
              htmlFor="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label id="password">Password</label>
            <input
              htmlFor="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" onClick={handleSubmit}>Sign-Up</button>
        </form>
        <div className="login-link">
          Already have an account? <Link to="/auth/login">Log In</Link> here.
        </div>
      </div>
    </div>
  );
};

export default Signup;
