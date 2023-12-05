import { useState, useEffect } from 'react';
import { useAddress, useContract, useContractRead } from "@thirdweb-dev/react";
import Card from './Card';
import Complaint from './Complaint';
import axios from 'axios';
import elliptic from 'elliptic';

const ec = new elliptic.ec('secp256k1');

const User = ({ keyPair }) => {
    const address = useAddress();
    const { contract } = useContract(process.env.REACT_APP_CONTRACT_ID);
    const { data } = useContractRead(contract, "getAllCases", [address]);
    const [sharedSecret, setSharedSecret] = useState(null);

    const getPublic = async () => {
        try {
            const response = await axios.get('http://localhost:3001/get-key/officer');

            const { key } = response.data;
            const loaded_key = ec.keyFromPublic(key, 'hex').getPublic();
            const sharedSecret = keyPair.derive(loaded_key);
            setSharedSecret(sharedSecret);
        } catch (error) {
            console.error('Error during authentication:', error);
        }
    }

    useEffect(() => {
        getPublic();
    }, [sharedSecret]);

    return (
        !data ? (
            <h1>Loading</h1>
        ) : (
            <>
                {
                    data.length === 0 ? (
                        <h1 className="gradient-text-1">No Complaints were Found</h1>
                    ) : (
                        <>
                            <h1 className="gradient-text-1">Complaints</h1>
                            <div className="grid">
                                {data.map((complaint, index) => (
                                    <Card key={index} complaint={complaint} secretKey={sharedSecret} />
                                ))}
                            </div>
                        </>
                    )
                }

                <Complaint secretKey={sharedSecret} />
            </>


        )

    );
};

export default User;