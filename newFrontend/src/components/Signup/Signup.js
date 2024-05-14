// Sign-Up.js
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Signup.css';

const Signup = () => {
  const [userType, setUserType] = useState('user');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [errorMsg, setErrorMsg] = useState('Please Try Again');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (userType === 'officer') {
        console.log('here')
        const url = `http://localhost:8081/signup/${userType}`;
        const body = {
          name: name,
          email: email,
          password: password,
        }
        const response = await axios.post(url, body);
        navigate('/auth/login');
        return;
      }
      else if (e.target.dept.value === '') {
        setError(true);
        setErrorMsg("Please choose your department")
        return;
      }
      else if (e.target.residence.value === '') {
        setError(true)
        setErrorMsg("Please choose your residence")
        return;
      }
      
      const url = `http://localhost:8081/signup/${userType}`;
      const body = {
        name: name,
        email: email,
        password: password,
        department: e.target.dept.value,
        residence: e.target.residence.value
      };

      const response = await axios.post(url, body);

      if (response.status !== 201) {
        throw Error('Could not signup');
      } else {
        navigate('/auth/login');
      }
      console.log(response)
    } catch (error) {
      setError(true);
    }
  };

  return (
    <div className="main-signup-form-container">
      <div className="signup-form-container">
        <form onSubmit={handleSubmit} className="signup-form">
          <h2>Sign-Up</h2>
          {error && <p className='error'>{errorMsg}</p>}
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
          {
            userType === 'user' &&
            <div>
              <div class="form-group">
                <label for="dept">Department</label>
                <select name="dept" id="dept" class="form-control">
                  <option value="" selected disabled hidden>Choose Your Department</option>
                  <option value="biotechnology">Biotechnology</option>
                  <option value="chemical engineering">Chemical Engineering</option>
                  <option value="chemistry">Chemistry</option>
                  <option value="civil engineering">Civil Engineering</option>
                  <option value="computer science and engineering">Computer Science and Engineering</option>
                  <option value="electrical engineering">Electrical Engineering</option>
                  <option value="electronics and communication">Electronics and Communication</option>
                  <option value="humanities and social science">Humanities and Social Science</option>
                  <option value="management studies">Management Studies</option>
                  <option value="mathematics">Mathematics</option>
                  <option value="mechanical engineering">Mechanical Engineering</option>
                  <option value="metallurgical and materials engineering">Metallurgical and Materials Engineering</option>
                  <option value="physics">Physics</option>
                  <option value="physical education">Physical Education</option>
                </select>
              </div>
              <div class="form-group">
                <label for="residence">Residence</label>
                <select name="residence" id="residence" class="form-control">
                  <option value="" selected disabled hidden>Choose Your Residence</option>
                  <option value="boyshostel">Boys Hostel</option>
                  <option value="girlshostel">Girls Hostel</option>
                  <option value="dayscholar">Day Scholar</option>
                </select>
              </div>
            </div>
          }
          <button type="submit">Sign-Up</button>
        </form>
        <div className="login-link">
          Already have an account? <Link to="/auth/login">Log In</Link> here.
        </div>
      </div>
    </div>
  );
};

export default Signup;
