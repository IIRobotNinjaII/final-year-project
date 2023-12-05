import { useState, useEffect } from 'react';
import { useContract, useContractRead, useContractWrite } from "@thirdweb-dev/react";
import Card from './Card';
import axios from 'axios';
import elliptic from 'elliptic';
import { encryptText } from '../utils/encrypt';
const ec = new elliptic.ec('secp256k1');

const Admin1 = ({ keyPair }) => {
    const [remark, setRemark] = useState("");
    const { contract } = useContract(process.env.REACT_APP_CONTRACT_ID);
    const { data: pendingReqComplaint } = useContractRead(contract, "getPendingReqComplaint")
    const { data: pendingReqs } = useContractRead(contract, "getPendingsReqs")
    const { mutateAsync: approveComplaint } = useContractWrite(contract, "approveComplaint")
    const { mutateAsync: disapproveComplaint } = useContractWrite(contract, "disapproveComplaint")

    const [sharedSecret, setSharedSecret] = useState(null);

    const getPublic = async (id) => {
        try {
            const response = await axios.get(`http://localhost:3001/get-key/${id}`);
            const { key } = response.data;
            const loaded_key = ec.keyFromPublic(key, 'hex').getPublic();
            const sharedSecret = keyPair.derive(loaded_key);
            setSharedSecret(sharedSecret);
        } catch (error) {
            console.error('Error during authentication:', error);
        }
    }

    const handleapproveComplaint = async () => {
        try {
            const data = await approveComplaint({ args: [encryptText(remark,sharedSecret)] });
            setRemark("");
            console.info("contract call successs", data);
        } catch (err) {
            console.error("contract call failure", err);
        }
    }

    const handledisapproveComplaint = async () => {
        try {
            const data = await disapproveComplaint({ args: [encryptText(remark,sharedSecret)] });
            setRemark("");
            console.info("contract call successs", data);
        } catch (err) {
            console.error("contract call failure", err);
        }
    }

    useEffect(() => {
        if(pendingReqs && pendingReqs.toString!=='200' && pendingReqComplaint)
            getPublic(pendingReqComplaint[1]);
    }, [pendingReqs, pendingReqComplaint, keyPair]);

    return (
        <>
            <h1 className="gradient-text-1">Officer 1</h1>
            {
                (!pendingReqs) ? (
                    <h1>Loading</h1>
                ) : (
                    <>
                        {
                            pendingReqs.toString() === '200' ? (
                                <>
                                    <h1>No Complaints to Approve</h1>
                                </>

                            ) : (
                                <>
                                    {sharedSecret && (
                                        <>
                                            <h1>Pending Complaints to be Approved : {pendingReqs.toString()}</h1>
                                            <Card complaint={pendingReqComplaint} secretKey={sharedSecret} />
                                            <button onClick={handleapproveComplaint}>Approve Complaint</button>
                                            <button onClick={handledisapproveComplaint}>Reject Complaint</button>
                                            <input type="text" placeholder='Enter Remark'
                                                onChange={(e) => { setRemark(e.target.value) }} />
                                        </>
                                    )}

                                </>
                            )
                        }
                    </>
                )
            }

        </>

    );
};

export default Admin1;