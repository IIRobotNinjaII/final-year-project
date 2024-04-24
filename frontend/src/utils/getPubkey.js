const getPublic = async () => {
    try {
        const response = await axios.get('http://localhost:3001/get-key/0xE1E016C5b5D0f205774b4DF0e0b591211ba2d729');

        const { key } = response.data;
        const loaded_key = ec.keyFromPublic(key, 'hex').getPublic();
        const sharedSecret = keyPair.derive(loaded_key);
        setSharedSecret(sharedSecret);
    } catch (error) {
        console.error('Error during authentication:', error);
    }
}