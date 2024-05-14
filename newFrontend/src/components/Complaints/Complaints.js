import React, { useState, useEffect, useCallback } from "react";
import SubmitComplaintForm from "../SubmitComplaint/SubmitComplaint";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEdit, faSignOut, faSync, faCheck, faXmark } from "@fortawesome/free-solid-svg-icons";
import { format } from 'date-fns';
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./complaints.css";

const Complaints = ({ userType, userDetails }) => {
  const [showSubmitForm, setShowSubmitForm] = useState(false);
  const [complaints, setComplaints] = useState([]);
  const [comment, setComment] = useState('');
  const [complaintId, setComplaintId] = useState(-1);
  const [complaintState, setComplaintState] = useState(true)
  const navigate = useNavigate();


  const fetchData = useCallback(async () => {
    console.log('fetching')
    try {
      let url = `http://localhost:8081/complaint/${userType === 'user' ? 'mycomplaints' : 'view'}`;

      const response = await axios.get(url, { withCredentials: true });

      setComplaints(response.data);
    } catch (error) {
      if (error.response.status === 404)
        setComplaints([])
      else
        navigate("/auth/login");
    }
  }, [userType, navigate]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handleToggleForm = () => {
    setShowSubmitForm(!showSubmitForm);
  };

  const handleSwitch = () => {
    setComplaintState(!complaintState)
  }
  const handleNavBack = () => {
    navigate("/");
  };

  const handleRefresh = async () => {
    fetchData();
    navigate("/complaints");
  }

  // const handleDeleteComplaint = () => {

  // }

  const handleComment = async (complaint_id) => {
    try {
      if (comment === '') {
        alert("Comment is empty");
        return;
      }
      const url = `http://localhost:8081/complaint/${complaint_id}`;
      const response = await axios.put(url, { comment }, { withCredentials: true });
      console.log(response.data)
      if (response.status !== 200) {
        throw new Error(response);
      } else {
        alert("Comment successful!!");
        setComment('');
        setComplaintId(-1);
      }
    } catch (error) {
      console.error(error);
      alert("Comment unsuccessful!")
    }
  }

  const setCommentState = (value, complaint_id) => {
    if (value !== '') {
      setComment(value);
      setComplaintId(complaint_id);
    }else{
      setComment('')
      setComplaintId(-1)
    }
  };

  const handleResolve = async (complaint_id) => {
    console.log('eh')

    try {
      const url = `http://localhost:8081/resolve-complaint/${complaint_id}`;
      const response = await axios.put(url, null, {
        withCredentials: true
    });

      if (response.status === 200) {
        alert("Complaint Resolved!! Yaaay!!");
      } else {
        throw new Error("Request Failed!!");
      }

    } catch (error) {
      console.log(error);
      alert('Could not resolve!');
    }
  }

  function renderSingleComplaint(complaint) {
    const formattedDate = format(new Date(complaint.created_at), "MMMM d, yyyy HH:mm:ss");
    return (
      <div key={complaint.id} className="complaint-card">
        <h3 className="complaint-id">Complaint ID: {complaint.id}</h3>
        <div className="complaint-details">
          <p>
            <b>Description: </b>
            {userType === 'user' ? complaint.description_user_copy : complaint.description}
          </p>
          <p>
            <b>Created At: </b>
            {String(formattedDate)}
          </p>
          <p>
            <b>Status: </b>
            {complaint.resolved ? "Resolved" : "Unresolved"}
          </p>
          {renderCommentSection(complaint.id, complaint)}


        </div>
        {/* <FontAwesomeIcon
        className="delete-complaint"
        icon={faTrashCan}
        onClick={handleDeleteComplaint(complaint.id)}
      /> */}
      </div >
    )
  }

  const renderComplaints = () => {

    let complaintElements = []
    if (complaintState) {
      let resolved = complaints.resolved;
      if (!resolved || Object.keys(resolved).length === 0)
        return <div className="no-complaints-found">No Resolved Complaints Found</div>

      for (var category in resolved) {
        complaintElements.push(
          <div className="category">
            <h2>{category}</h2>
          </div>
        )
        for (var cmp in resolved[category])
          complaintElements.push(renderSingleComplaint(resolved[category][cmp]));
      }
    } else {
      let unresolved = complaints.unresolved;
      if (!unresolved || Object.keys(unresolved).length === 0)
        return <div className="no-complaints-found">No Unresolved Complaints Found</div>

      for (category in unresolved) {
        complaintElements.push(
          <div className="category">
            <h2>{category}</h2>
          </div>
        )
        for (cmp in unresolved[category])
          complaintElements.push(renderSingleComplaint(unresolved[category][cmp]));
      }
    }


    return complaintElements;
  };

  const renderCommentSection = (complaint_id, complaint) => {
    let comments = complaint?.comments;
    if (comments){
      
      return (
        <div className="comment-section">
          < ul >
            {
              comments.map((comment) => {
                return (
                  <li className="comment">
                    <div className="comment-header">
                      <span className="comment-author">Officer ID : {comment.author_id}</span>
                      <span className="comment-date">{format(new Date(comment.created_at), "MMMM d, yyyy HH:mm:ss")}</span>
                    </div>
                    <div className="comment-content">
                      {(userType === 'user') ? comment.comment_user_copy : comment.comment}
                    </div>
                  </li>
                )
              })
            }
          </ul >
          {(userType !== 'user' && !complaint.resolved ) && <div>
            <textarea
              value={(complaint_id === complaintId) ? comment : ''}
              onChange={(e) => setCommentState(e.target.value, complaint_id)}
              placeholder="Enter your comment here"
            ></textarea>
            <div>
              <button className="submit-button" onClick={() => handleComment(complaint_id)}>Submit</button>
              <button className="resolve-button" onClick={() => handleResolve(complaint_id)}>Resolve</button>
            </div>
          </div>}
        </div >
      );
    }
  };


  return (
    <div className="main-container">
      <div data-aos="fade-left" className="complaint-container">
        <div className="header">
          <FontAwesomeIcon
            className="refresh-btn header-btn"
            icon={faSync}
            onClick={handleRefresh}
          />
          <FontAwesomeIcon
            className={`logout-btn header-btn ${complaintState ? 'selected' : ''}`}
            icon={faCheck}
            onClick={handleSwitch}
          />
          <FontAwesomeIcon
            className={`logout-btn header-btn ${!complaintState ? 'selecte' : ''}`}
            icon={faXmark}
            onClick={handleSwitch}
          />
          {/* <p className="undo-button header-btn">logout</p> */}
          <h1 className="complaint-heading">Complaints</h1>
          {userType === "user" && (
            <FontAwesomeIcon
              className="submit-complaint-button header-btn"
              icon={faEdit}
              onClick={handleToggleForm}
            />
          )}
          <FontAwesomeIcon
            className="logout-btn header-btn"
            icon={faSignOut}
            onClick={handleNavBack}
          />
        </div>
        {renderComplaints()}
      </div>
      {showSubmitForm && (
        <div data-aos="fade-left" className="submit-complaint-form">
          <SubmitComplaintForm fetchData={fetchData}/>
        </div>
      )}
    </div>
  );
};

export default Complaints;
