import React, { useState } from 'react';
import { useContract, useContractWrite } from "@thirdweb-dev/react";
import { encryptText } from '../utils/encrypt';

const Complaint = ({secretKey}) => {
    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [name,setName] = useState("");
    const [dept,setDept] = useState("");
    const [rollno, setRollno] = useState("");

    const { contract } = useContract(process.env.REACT_APP_CONTRACT_ID);
    const { mutateAsync: fileComplaint, isLoading } = useContractWrite(contract, "fileComplaint");

    const handleComplaint = async () => {
        try {
            const data = await fileComplaint({ args: [encryptText(title,secretKey), encryptText(description,secretKey), encryptText(name,secretKey), encryptText(dept,secretKey), encryptText(rollno,secretKey)] });
            console.info("contract call successs", data);
            setTitle("");
            setDescription("");
            setName("");
            setDept("");
            setRollno("");
        } catch (err) {
            console.error("contract call failure", err);
        }
    }

    return (
        <div className="card complaint">
            <div className="card-text">
                <h1>File your Complaint Here</h1>
                <p>Enter Complaint Title : </p>
                <input type="text" placeholder='Enter Title Here'
                    onChange={(e) => { setTitle(e.target.value) }} />
                <p>Enter Complaint Description : </p>
                <input type="text" placeholder='Enter Description Here'
                    onChange={(e) => { setDescription(e.target.value) }} />
                <p>Enter Name : </p>
                <input type="text" placeholder='Enter Name Here'
                    onChange={(e) => { setName(e.target.value) }} />
                <p>Enter Roll No : </p>
                <input type="text" placeholder='Enter Roll No'
                    onChange={(e) => { setRollno(e.target.value) }} />
                <p>Enter Department : </p>
                <input type="text" placeholder='Enter Department'
                    onChange={(e) => { setDept(e.target.value) }} />
                <button onClick={handleComplaint}>File Complaint</button>
            </div>
        </div>
    )
}

export default Complaint;