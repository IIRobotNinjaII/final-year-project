import CryptoJS from 'crypto-js';

export const decryptText = (enctext, sharedSecret) => {
    try {
        const iv = CryptoJS.enc.Hex.parse('0123456789ABCDEF0123456789ABCDEF');
        const key = CryptoJS.enc.Hex.parse(sharedSecret.toString('hex'));
        const decrypted = CryptoJS.AES.decrypt(enctext.toString(), key, { iv, mode: CryptoJS.mode.CBC, padding: CryptoJS.pad.Pkcs7 });
        return decrypted.toString(CryptoJS.enc.Utf8);
    }

    catch (err) {
        return enctext;
    }
};