import React, { useState, useEffect } from 'react';
import { useContract, useContractRead, useContractWrite } from "@thirdweb-dev/react";
import Card from './Card';
import axios from 'axios';
import elliptic from 'elliptic';
import { encryptText } from '../utils/encrypt';
const ec = new elliptic.ec('secp256k1');

const Admin3 = ({ keyPair }) => {
    const [remark, setRemark] = useState("");
    const { contract } = useContract(process.env.REACT_APP_CONTRACT_ID);
    const { data: pendingResComplaint } = useContractRead(contract, "getPendingResComplaint")
    const { data: pendingRes } = useContractRead(contract, "getPendingsRes")
    const { mutateAsync: resolveComplaint } = useContractWrite(contract, "resolveComplaint")
    const [sharedSecret, setSharedSecret] = useState(null);

    const handleActionClick = async () => {
        try {
            const data = await resolveComplaint({ args: [encryptText(remark, sharedSecret)] });
            console.info("contract call successs", data);
        } catch (err) {
            console.error("contract call failure", err);
        }
    }

    const getPublic = async (id) => {
        try {
            const response = await axios.get(`http://localhost:3001/get-key/${id}`);
            const { key } = response.data;
            const loaded_key = ec.keyFromPublic(key, 'hex').getPublic();
            const calculatedSharedSecret = keyPair.derive(loaded_key);
            setSharedSecret(calculatedSharedSecret);
        } catch (error) {
            console.error('Error during authentication:', error);
        }
    };

    useEffect(() => {
        if (pendingRes && pendingRes.toString() !== '200' && pendingResComplaint) {
            getPublic(pendingResComplaint[1]);
        }
    }, [pendingRes, pendingResComplaint, keyPair]);

    return (
        <>
            <h1 className="gradient-text-1">Officer 3</h1>
            {
                (!pendingRes) ? (
                    <h1>Loading</h1>
                ) : (
                    <>
                        {
                            pendingRes.toString() === '200' ? (
                                <h1>No Complaints to Resolve</h1>
                            ) : (
                                sharedSecret && (
                                    <>
                                        <h1>Pending Complaints to be Resolved : {pendingRes.toString()}</h1>
                                        <Card complaint={pendingResComplaint} secretKey={sharedSecret} />
                                        <input type="text" placeholder='Enter Remark'
                                            onChange={(e) => { setRemark(e.target.value) }} />
                                        <button onClick={handleActionClick}>Submit</button>
                                    </>
                                )

                            )
                        }
                    </>
                )
            }

        </>

    );
};

export default Admin3;