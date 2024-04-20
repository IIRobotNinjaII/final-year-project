from flask import Flask, jsonify, request
import os
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

app = Flask(__name__)

# Store user data with associated public keys
users = {
    "user1": {
        "password": "password1",
        "public_key": None,
        "policy": "A OR B"
    },
    "user2": {
        "password": "password2",
        "public_key": None,
        "policy": "A AND B"
    }
}

# Generate private and public key for Diffie-Hellman
parameters = dh.generate_parameters(generator=2, key_size=512)
private_key = parameters.generate_private_key()
public_key = private_key.public_key()

# Derive a 256-bit shared key using HKDF
kdf = HKDF(
    algorithm=hashes.SHA256(),
    length=32,  # 32 bytes = 256 bits
    salt=None,  # Not required for DH key exchange
    info=b'derived_key',
    backend=default_backend()
)


def encrypt_key(user_policy_based_key, derived_key):
    print(derived_key)
    print(user_policy_based_key)
    user_policy_based_key = user_policy_based_key.encode('utf-8')
    print(user_policy_based_key)

    # Ensure the key is exactly 32 bytes (256 bits) as required by AES-256
    if len(derived_key) != 32:
        raise ValueError("Key must be 32 bytes (256 bits) long.")

    # Create an AES cipher with ECB mode
    cipher = Cipher(algorithms.AES(derived_key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad the user_policy_based_key to be a multiple of 16 bytes (AES block size)
    if len(user_policy_based_key) % 16 != 0:
        user_policy_based_key += b' ' * (16 - len(user_policy_based_key) % 16)

    # Encrypt the padded user_policy_based_key
    encrypted_user_policy_based_key = encryptor.update(user_policy_based_key) + encryptor.finalize()

    print(encrypted_user_policy_based_key)
    encrypted_user_policy_based_key = encrypted_user_policy_based_key.hex()
    print(encrypted_user_policy_based_key)

    return encrypted_user_policy_based_key

@app.route('/get_public_key', methods=['GET'])
def get_public_key():
    # Serialize and send public key
    serialized_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return jsonify({'public_key': serialized_key.decode()}), 200

@app.route('/login', methods=['POST'])
def login():
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        return jsonify({'error': 'Missing username or password'}), 400

    username = request.json['username']
    password = request.json['password']

    if username not in users or users[username]['password'] != password:
        return jsonify({'error': 'Invalid credentials'}), 401

    users[username]['public_key'] = serialization.load_pem_public_key(
        request.json['public_key'].encode(),
    )

    return jsonify({'user_policy_based_key': 'Login successful'}), 200

@app.route('/get_shared_key', methods=['POST'])
def get_shared_key():
    if not request.json or 'username' not in request.json:
        return jsonify({'error': 'Missing username'}), 400

    username = request.json['username']

    if username not in users or users[username]['public_key'] is None:
        return jsonify({'error': 'Public key not available for the user'}), 404

    # Deserialize user's public key
    user_public_key = users[username]['public_key']
    user_policy = users[username]['policy']

    # Compute shared key
    shared_key = private_key.exchange(user_public_key)
    derived_key = kdf.derive(shared_key)

    print(derived_key.hex())
    return jsonify({'derived_key': derived_key.hex() }), 200 #,'encrypted_policy': encrypt_key(user_policy,derived_key.hex())}

if __name__ == '__main__':
    app.run(debug=True, port=8080)
