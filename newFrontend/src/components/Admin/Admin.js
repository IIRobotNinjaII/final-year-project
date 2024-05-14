import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import "./Admin.css"

const Admin = () => {
    const [users, setUsers] = useState([]);
    const [policy, setPolicy] = useState('');
    const [userId, setUserId] = useState(-1);
    
    const fetchData = useCallback(async () => {
        console.log('fetching')
        try {
            let url = 'http://localhost:8081/admin/users';

            const response = await axios.get(url);
            // console.log(response.data["unapproved_officer"])
            setUsers(response.data["unapproved_officer"]);
        } catch (error) {
            if (error.response.status === 404)
                setUsers([])
        }
    }, []);

    useEffect(() => {
        fetchData();
    }, [fetchData]);

    const setPolicyState = (value,user_id) => {
        if (value !== '') {
            setPolicy(value);
            setUserId(user_id);
        } else {
            setPolicy('');
            setUserId(-1);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
          if (policy === '') {
            alert("Policy is empty");
            return;
          }

          const url = `http://localhost:8081/admin/approve/${userId}`;

          let body = {
            policy : policy,
            usertype : 'officer'
          }

          const response = await axios.put(url, { policy : policy, usertype : "officer" }, { withCredentials: true });
          console.log(response.data)
          if (response.status !== 200) {
            throw new Error(response);
          } else {
            alert("Officer Approved");
            setPolicy('');
          }
        } catch (error) {
          console.error(error);
          alert("Officer approval unsuccessful!")
        }
      }

    return (
        <div className="comment-container">
            <div className="header">

                {/* <p className="undo-button header-btn">logout</p> */}
                <h1 className="complaint-heading">Admin Portal</h1>

            </div>
            {
                !users ? (
                    <div className="no-complaints-found">No officers found.</div>
                ) : (

                    users.map(user => (
                        <div key={user.id} >
                            <div className="admin-card">
                                <div className="admin-id">Officer ID : {user.id}</div>
                                <div className="admin-details">
                                    <div>Name: {user.name}</div>
                                    <div>Email: {user.email}</div>
                                    <form>
                                        <textarea className="admin-section" placeholder="Enter Policy" rows={1} cols={2} onChange={(e) => setPolicyState(e.target.value,user.id)} required></textarea>
                                        <button className="submit-button" onClick={handleSubmit}>Submit</button>
                                    </form>
                                </div>
                            </div>
                        </div>
                    ))

                )
            }

        </div>
    );
};

export default Admin;
