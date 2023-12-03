import React, { useState } from 'react';
import { useContract, useContractRead, useContractWrite } from "@thirdweb-dev/react";
import Card from './Card';
const Admin2 = () => {
    const [remark, setRemark] = useState("");
    const { contract } = useContract("0x811e46292aF2Af63ac15553E0Ec7Ac3fd4871377");
    const { data : pendingActionComplaint } = useContractRead(contract, "getPendingActionComplaint")
    const { data : pendingActions } = useContractRead(contract, "getPendingsActions")
    const { mutateAsync: takeAction } = useContractWrite(contract, "takeAction")

    const handleActionClick = async () => {
        try {
          const data = await takeAction({ args: [remark] });
          console.info("contract call successs", data);
          setRemark("");
        } catch (err) {
          console.error("contract call failure", err);
        }
      }

    return (
        <>
            <h1 className="gradient-text-1">Officer 2</h1>
            {
                (!pendingActions) ? (
                    <h1>Loading</h1>
                ) : (
                    <>
                        {
                            pendingActions.toString() === '200' ? (
                                <h1>No Complaints to Take Action</h1>
                            ) : (
                                <>
                                    <h1>Pending Complaints to Take Action : {pendingActions.toString()}</h1>
                                    <Card  complaint={pendingActionComplaint} />
                                    <input type="text" placeholder='Enter Remark'
                                        onChange={(e) => { setRemark(e.target.value) }} />
                                    <button onClick={handleActionClick}>Submit</button>
                                </>
                            )
                        }
                    </>  
                )
            }

        </>

    );
};

export default Admin2;