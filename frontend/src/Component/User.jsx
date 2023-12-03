import React from 'react';
import { useAddress, useContract, useContractRead } from "@thirdweb-dev/react";
import Card from './Card';
import Complaint from './Complaint';
const User = () => {
    const address = useAddress();
    const { contract } = useContract("0x811e46292aF2Af63ac15553E0Ec7Ac3fd4871377");
    const { data } = useContractRead(contract, "getAllCases", [address]);
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
                                    <Card key={index} complaint={complaint} />
                                ))}
                            </div>
                        </>
                    )
                }
                
                <Complaint />
            </>


        )

    );
};

export default User;