import React , { useState }  from 'react';
import { useContract, useContractRead, useContractWrite } from "@thirdweb-dev/react";
import Card from './Card';
const Admin1 = () => {
    const [remark, setRemark] = useState("");
    const { contract } = useContract("0x811e46292aF2Af63ac15553E0Ec7Ac3fd4871377");
    const { data: pendingReqComplaint } = useContractRead(contract, "getPendingReqComplaint")
    const { data: pendingReqs } = useContractRead(contract, "getPendingsReqs")
    const { mutateAsync: approveComplaint } = useContractWrite(contract, "approveComplaint")
    const { mutateAsync: disapproveComplaint } = useContractWrite(contract, "disapproveComplaint")

    const handleapproveComplaint = async () => {
        try {
            const data = await approveComplaint({ args: [remark] });
            setRemark("");
            console.info("contract call successs", data);
        } catch (err) {
            console.error("contract call failure", err);
        }
    }

    const handledisapproveComplaint = async () => {
        try {
            const data = await disapproveComplaint({ args: [remark] });
            setRemark("");
            console.info("contract call successs", data);
        } catch (err) {
            console.error("contract call failure", err);
        }
    }

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
                                <h1>No Complaints to Approve</h1>
                            ) : (
                                <>
                                    <h1>Pending Complaints to be Approved : {pendingReqs.toString()}</h1>
                                    <Card complaint={pendingReqComplaint} />
                                    <button onClick={handleapproveComplaint}>Approve Complaint</button>
                                    <button onClick={handledisapproveComplaint}>Reject Complaint</button>
                                    <input type="text" placeholder='Enter Remark'
                                        onChange={(e) => { setRemark(e.target.value) }} />
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