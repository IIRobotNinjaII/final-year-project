import React, { useState, useEffect } from 'react';
import { useContract, useContractRead, useContractWrite } from "@thirdweb-dev/react";
import Card from './Card';
import axios from 'axios';
import elliptic from 'elliptic';
import { encryptText } from '../utils/encrypt';
const ec = new elliptic.ec('secp256k1');

const Admin2 = ({ keyPair }) => {
    const [remark, setRemark] = useState("");
    const { contract } = useContract(process.env.REACT_APP_CONTRACT_ID);
    const { data: pendingActionComplaint } = useContractRead(contract, "getPendingActionComplaint");
    const { data: pendingActions } = useContractRead(contract, "getPendingsActions");
    const { mutateAsync: takeAction } = useContractWrite(contract, "takeAction");
    const [sharedSecret, setSharedSecret] = useState(null);

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

    const handleActionClick = async () => {
        try {
            const data = await takeAction({ args: [encryptText(remark,sharedSecret)] });
            console.info("contract call success", data);
            setRemark("");
        } catch (err) {
            console.error("contract call failure", err);
        }
    };

    useEffect(() => {
        if (pendingActions && pendingActions.toString() !== '200' && pendingActionComplaint) {
            getPublic(pendingActionComplaint[1]);
        }
    }, [pendingActions, pendingActionComplaint, keyPair]);

    return (
        <>
            <h1 className="gradient-text-1">Officer 2</h1>
            {!pendingActions ? (
                <h1>Loading</h1>
            ) : (
                <>
                    {pendingActions.toString() === '200' ? (
                        <h1>No Complaints to Take Action</h1>
                    ) : (
                        sharedSecret && (
                            <>
                                <h1>Pending Complaints to Take Action: {pendingActions.toString()}</h1>
                                <Card complaint={pendingActionComplaint} secretKey={sharedSecret} />
                                <input type="text" placeholder='Enter Remark' onChange={(e) => { setRemark(e.target.value) }} />
                                <button onClick={handleActionClick}>Submit</button>
                            </>
                        )
                    )}
                </>
            )}
        </>
    );
};

export default Admin2;
