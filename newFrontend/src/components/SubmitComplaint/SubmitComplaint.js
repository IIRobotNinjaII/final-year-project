import React, { useState } from 'react';
import axios from 'axios';
import './SubmitComplaintForm.css';

const SubmitComplaintForm = () => {
  const [body, setBody] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setBody({
      ...body,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8080/complaint/file', body, { withCredentials: true });
      if (response.status !== 201) {
        throw new Error('Failed to submit complaint');
      }
      setBody({});
      alert('Complaint submitted successfully!');
    } catch (error) {
      console.error('Error submitting complaint:', error);
      alert('Failed to submit complaint. Please try again later.');
    }
  };

  return (
    <div className="form-container">
      <h1>Submit New Complaint</h1>
      <form onSubmit={handleSubmit} className="main-form">
        <div className="form-group">
          {/* Complaint Description */}
          <textarea
            id="complaint-description"
            className="complaint-description"
            name="text"
            value={body.text}
            onChange={handleChange}
            placeholder="Complaint Description"
            required
          />
        </div>

        <div className="form-group">
          {/* Category Selection */}
          <label>Category</label>
          <div className="radio-buttons">
            <input
              type="radio"
              id="category-residential"
              className="form-check-input"
              name="category"
              value="residential"
              onChange={handleChange}
              checked={body.category === 'Accounting'}
            />
            <label htmlFor="category-residential">Residential</label>

            <input
              type="radio"
              id="category-academic"
              className="form-check-input"
              name="category"
              value="academic"
              onChange={handleChange}
              checked={body.category === 'Academic'}
            />
            <label htmlFor="category-academic">Academic</label>

            <input
              type="radio"
              id="category-account"
              className="form-check-input"
              name="category"
              value="account"
              onChange={handleChange}
              checked={body.category === 'account'}
            />
            <label htmlFor="category-account">Account</label>
          </div>
        </div>

        {/* Submit Button */}
        <button type="submit" className="btn btn-primary submit-button">
          Submit Complaint
        </button>
      </form>
    </div>
  );
};

export default SubmitComplaintForm;
