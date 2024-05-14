import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from 'react-router-dom';
import "./SubmitComplaintForm.css";

const SubmitComplaintForm = ({fetchData}) => {
  const [text, setText] = useState("");
  const [category, setCategory] = useState("");
  const [subCategory, setSubCategory] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const url = "http://localhost:8081/complaint/file";

      const body = {
        text,
        "complaint type": category,
      };

      if(category === 'account')
        body[`${category} complaint type`] = subCategory;
      else if(category === 'residential')
        body[`${category} complaint type`] = subCategory;

      const response = await axios.post(
        url,
        body,
        { withCredentials: true }
      );

      // if (response.status !== 201) {
      //   console.log(response);
      //   throw new Error('Request Unsuccessful!!');
      // }

      setText('');
      setCategory('');
      setSubCategory('');
      navigate('/complaints');
      alert('Complaint Filed!');
      await fetchData();
    } catch (error) {
      alert(error);
      console.log(error);
    }
  };

  return (
    <div className="form-container">
      <h1 className="submit-form-heading">Submit New Complaint</h1>
      <form onSubmit={handleSubmit} className="main-form">
        <div className="sc-form-group">

          <div>
            <select
              value={category}
              onChange={(e) => {setCategory(e.target.value); setSubCategory('')}}
              className="category-select"
              required
            >
              <option value="" selected disabled >Choose Your Category</option>
              <option value="account">Account</option>
              <option value="academic">Academic</option>
              <option value="residential">Residential</option>
            </select>
          </div>
          {category === 'account' ? (
            <select
              value={subCategory}
              onChange={(e) => setSubCategory(e.target.value)}
              className="category-select"
              style={{ marginTop: '10px' }}
              required
            >
              <option value="" selected disabled >Select Dues/Refund</option>
              <option value="due">Due</option>
              <option value="refund">Refund</option>
            </select>
          ) : category === 'residential' ? (
            <select
              value={subCategory}
              onChange={(e) => setSubCategory(e.target.value)}
              className="category-select"
              style={{ marginTop: '10px' }}
              required
            >
              <option value="" selected disabled>Select type of issue</option>
              <option value="electric">Electrical</option>
              <option value="plumbing">Plumbing</option>
              <option value="network">Network</option>
            </select>
          ) : null}
        </div>
        <div className="sc-form-group">
          {/* Complaint Description */}
          <textarea
            id="text"
            className="complaint-text"
            name="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Complaint Description"
            required
          />
          <label htmlFor="text" />
        </div>

        {/* Submit Button */}
        <button type="submit" className="submit-form-button">
          Submit Complaint
        </button>
      </form>
    </div>
  );
};

export default SubmitComplaintForm;
