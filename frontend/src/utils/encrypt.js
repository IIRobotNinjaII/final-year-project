import CryptoJS from 'crypto-js';

export const encryptText = async (text, sharedSecret) =>{
    const iv = CryptoJS.enc.Hex.parse('0123456789ABCDEF0123456789ABCDEF');
    const key = CryptoJS.enc.Hex.parse(sharedSecret.toString('hex'));
    const encrypted = CryptoJS.AES.encrypt(text, key, { iv, mode: CryptoJS.mode.CBC, padding: CryptoJS.pad.Pkcs7 });
    return encrypted.toString();
  }