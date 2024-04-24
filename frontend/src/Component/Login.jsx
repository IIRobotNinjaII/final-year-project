import { useState, useEffect } from 'react';
import { useAddress, useContractRead , useContract } from "@thirdweb-dev/react";
import axios from 'axios';
import CryptoJS from 'crypto-js';
import elliptic from 'elliptic';
import Admin1 from "./Admin1";
import Admin2 from "./Admin2";
import Admin3 from "./Admin3";
import User from "./User";

const ec = new elliptic.ec('secp256k1');


const Login = () => {
    const address = useAddress();
    const { contract } = useContract(process.env.REACT_APP_CONTRACT_ID);
    const { data: officer1 } = useContractRead(contract, "officer1");
    const { data: officer2 } = useContractRead(contract, "officer2");
    const { data: officer3 } = useContractRead(contract, "officer3");
    const [previousAddress, setPreviousAddress] = useState(address);
    const [password, setPassword] = useState('');
    const [authenticated, setAuthenticated] = useState(false);
    const [keyPair, setKeyPair] = useState(null);

    useEffect(() => {
        if (address !== previousAddress) {
            setPreviousAddress(address);
            setAuthenticated(false);
        }
    }, [address, previousAddress]);

    const handleLogin = async () => {
        const priv = CryptoJS.SHA256(password);
        const temp_keyPair = ec.keyFromPrivate(priv.toString(), 'hex');
        const key_pub = temp_keyPair.getPublic();

        try {
            const response = await axios.post('http://localhost:3001/authenticate', {
                userId: previousAddress,
                passwordHash: CryptoJS.SHA512(password).toString(),
                key: key_pub.encode('hex', true),
            });

            const { key } = response.data;
            if (key === 0) {
                alert('Authentication failed. Please try again.');
            } else if (key === 2) {
                alert('Account Created Successfully');
                setPassword('');
                setKeyPair(temp_keyPair);
                setAuthenticated(true);
            } else {
                setKeyPair(temp_keyPair)
                setPassword('');
                setAuthenticated(true);
            }
        } catch (error) {
            console.error('Error during authentication:', error);
        }


    };

    return (
        !authenticated ? (
            <div>
                <label>
                    Password:
                    <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
                </label>
                <br />
                <button onClick={handleLogin}>Login</button>
            </div>
        ) : (officer1 && officer2 && officer3 && (
            (officer1 === address) ? (
                <Admin1 keyPair={keyPair} />
            ) : (officer2 === address) ? (
                <Admin2 keyPair={keyPair} />
            ) : (officer3 === address) ? (
                <Admin3 keyPair={keyPair} />
            ) : (
                <User keyPair={keyPair} />
            )
        )

        )
    );

}

export default Login;