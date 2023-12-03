import React, { useState } from 'react';
import { useContract, useContractRead, useContractWrite } from "@thirdweb-dev/react";
import Card from './Card';
const Admin2 = () => {
    const [remark, setRemark] = useState("");
    const { contract } = useContract("0x811e46292aF2Af63ac15553E0Ec7Ac3fd4871377");
    const { data : pendingResComplaint} = useContractRead(contract, "getPendingResComplaint")
    const { data : pendingRes} = useContractRead(contract, "getPendingsRes")
    const { mutateAsync: resolveComplaint } = useContractWrite(contract, "resolveComplaint")

  const handleActionClick = async () => {
    try {
      const data = await resolveComplaint({ args: [remark] });
      console.info("contract call successs", data);
    } catch (err) {
      console.error("contract call failure", err);
    }
  }
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
                                <>
                                    <h1>Pending Complaints to be Resolved : {pendingRes.toString()}</h1>
                                    <Card  complaint={pendingResComplaint} />
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