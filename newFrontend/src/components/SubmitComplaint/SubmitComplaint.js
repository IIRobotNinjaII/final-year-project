import React, { useState } from 'react';
import './SubmitComplaintForm.css';

const SubmitComplaintForm = () => {
  const [formData, setFormData] = useState({
    text: '',
    category: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/complaint/file', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      if (!response.ok) {
        throw new Error('Failed to submit complaint');
      }
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
            value={formData.text}
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
              id="category-accounting"
              className="form-check-input"
              name="category"
              value="Accounting"
              onChange={handleChange}
              checked={formData.category === 'Accounting'}
            />
            <label htmlFor="category-accounting">Accounting</label>

            <input
              type="radio"
              id="category-academic"
              className="form-check-input"
              name="category"
              value="Academic"
              onChange={handleChange}
              checked={formData.category === 'Academic'}
            />
            <label htmlFor="category-academic">Academic</label>

            <input
              type="radio"
              id="category-hostel"
              className="form-check-input"
              name="category"
              value="Hostel"
              onChange={handleChange}
              checked={formData.category === 'Hostel'}
            />
            <label htmlFor="category-hostel">Hostel</label>
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
