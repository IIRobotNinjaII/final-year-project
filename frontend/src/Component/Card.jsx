import React from 'react';

const Card = ({ complaint }) => {
    return (

        <div className="card">
            <div className="card-text">
                <h2 className="gradient-text-1">Title : {complaint[2]}</h2>
                <h3 className='gradient-text-2'>Name : {complaint[4]}</h3>
                <h3 className='gradient-text-3'>Roll Number : {complaint[6]}</h3>
                <h3 className='gradient-text-0'>Department : {complaint[5]}</h3>
                <h3>
                    {complaint[3]}
                </h3>

                {!complaint[10] ? (
                    <h3>{complaint[7]}</h3>
                ) : (
                <>
                    <h3>Approved ✅ : {complaint[7]}</h3>
                    {
                        !complaint[11] ? (
                            <h3>{complaint[8]}</h3>
                        ) : (
                            <>
                                <h3>Action Taken ✅: {complaint[8]}</h3>
                                {
                                    !complaint[12] ? (
                                        <h3>{complaint[9]}</h3>
                                    ) : (
                                        <h3>Resolved ✅ : {complaint[9]} </h3>
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