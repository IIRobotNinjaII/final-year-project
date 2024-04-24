import React, { useState, useEffect } from 'react';
import SubmitComplaintForm from '../SubmitComplaint/SubmitComplaint';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEdit, faArrowLeft } from '@fortawesome/free-solid-svg-icons';
import axios from 'axios';
import './complaints.css';

const Complaints = ({ userType }) => {
  const [showSubmitForm, setShowSubmitForm] = useState(false);
  const [complaints, setComplaints] = useState([]);

  useEffect(() => {

    const fetchData = async () => {
      try {
        const fetchedData = await axios.get(
          `http://localhost:8080/complaint/${
            userType === 'user' ? 'mycomplaints' : 'view'
          }`,
          { withCredentials: true }
        );

        setComplaints(fetchedData.data.complaints);
        console.log(userType);
      } catch (error) {
        console.error(error);
      }
    };

    fetchData();
  }, [userType]);

  const handleToggleForm = () => {
    setShowSubmitForm(!showSubmitForm);
  };

  const handleNavback = () => {
    localStorage.clear();
    window.location.reload();
  };

  return (
    <div className="main-container">
      <div data-aos="fade-left" className="complaint-container">
        <div className="header">
          <FontAwesomeIcon
            className="undo-button header-btn"
            icon={faArrowLeft}
            onClick={handleNavback}
          />
          <h1 className='complaint-heading'>Complaints</h1>
          { (userType === 'user') && <FontAwesomeIcon
            className="submit-complaint-button header-btn"
            icon={faEdit}
            onClick={handleToggleForm}
          />}
        </div>
        {complaints.map((complaint) => (
          <div key={complaint.complaint.id} className="complaint-card">
            <h3>{complaint.complaint.id}</h3>
            <div className="complaint-details">
              <div className="description created-at status">
                <div className="comments">
                  <p>
                    <b>Description: </b>
                    {complaint.complaint.description_user_copy}
                  </p>
                  <p>
                    <b>Created At: </b>
                    {String(complaint.complaint.created_at)}
                  </p>
                  <p>
                    <b>Status: </b>
                    {complaint.complaint.resolved ? 'Resolved' : 'Unresolved'}
                  </p>
                  {userType === 'officer' && (
                    <div className="comment-section">
                      <textarea placeholder="Enter your comment here "></textarea>
                      <button>Submit</button>
                    </div>
                  )}
                  {/* Add more complaint details here */}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
      {showSubmitForm && (
        <div data-aos="fade-left" className="submit-complaint-form">
          <SubmitComplaintForm />
        </div>
      )}
    </div>
  );
};

export default Complaints;
