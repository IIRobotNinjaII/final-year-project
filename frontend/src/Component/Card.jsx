import React from 'react';
import { decryptText } from '../utils/decrypt';


const Card = ({ complaint, secretKey }) => {
    return (

        <div className="card">
            <div className="card-text">
                <h2 className="gradient-text-1">Title : {decryptText(complaint[2],secretKey)}</h2>
                <h3 className='gradient-text-2'>Name : {decryptText(complaint[4],secretKey)}</h3>
                <h3 className='gradient-text-3'>Roll Number : {decryptText(complaint[6],secretKey)}</h3>
                <h3 className='gradient-text-0'>Department : {decryptText(complaint[5],secretKey)}</h3>
                <h3>
                    {decryptText(complaint[3],secretKey)}
                </h3>

                {!complaint[10] ? (
                    <h3>{decryptText(complaint[7],secretKey)}</h3>
                ) : (
                    <>
                        <h3>Approved ✅ : {decryptText(complaint[7],secretKey)}</h3>
                        {
                            !complaint[11] ? (
                                <h3>{complaint[8]}</h3>
                            ) : (
                                <>
                                    <h3>Action Taken ✅: {decryptText(complaint[8],secretKey)}</h3>
                                    {
                                        !complaint[12] ? (
                                            <h3>{complaint[9]}</h3>
                                        ) : (
                                            <h3>Resolved ✅ : {decryptText(complaint[9],secretKey)} </h3>
                                        )
                                    }
                                </>
                            )
                        }

                    </>
                )}

            </div>
        </div>

    );
};

export default Card;