import requests
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Replace these values with the actual server address
SERVER_ADDRESS = 'http://localhost:8080'

# Dummy user credentials for testing
username = 'user1'
password = 'password1'

# Generate private and public key for Diffie-Hellman
parameters = dh.generate_parameters(generator=2, key_size=512)
private_key = parameters.generate_private_key()
public_key = private_key.public_key()

def decrypt_message(encrypted_message, key):
    print(key)
    print(encrypted_message)
    encrypted_message= bytes.fromhex(encrypted_message)
    print(encrypted_message)

    # Ensure the key is exactly 32 bytes (256 bits) as required by AES-256
    if len(key) != 32:
        raise ValueError("Key must be 32 bytes (256 bits) long.")

    # Create an AES cipher with ECB mode
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the encrypted message
    decrypted_message = decryptor.update(encrypted_message) + decryptor.finalize()
    print(decrypted_message)
    decrypted_message = decrypted_message.decode('utf-8')
    print(decrypted_message)

    return decrypted_message

# Derive a 256-bit shared key using HKDF
kdf = HKDF(
    algorithm=hashes.SHA256(),
    length=32,  # 32 bytes = 256 bits
    salt=None,  # Not required for DH key exchange
    info=b'derived_key',
    backend=default_backend()
)

def get_server_public_key():
    response = requests.get(f"{SERVER_ADDRESS}/get_public_key")
    if response.status_code == 200:
        server_public_key = serialization.load_pem_public_key(
            response.json()['public_key'].encode(),
        )
        return server_public_key
    else:
        print("Failed to get server public key")
        return None

def login(username, password, public_key):
    data = {
        'username': username,
        'password': password,
        'public_key': public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()
    }
    response = requests.post(f"{SERVER_ADDRESS}/login", json=data)
    if response.status_code == 200:
        print("Login successful")
        return True
    else:
        print("Login failed")
        return False

def get_shared_key(username, public_key):
    data = {'username': username}
    response = requests.post(f"{SERVER_ADDRESS}/get_shared_key", json=data)
    if response.status_code == 200:
        derived_key = response.json()['derived_key']
        # encrypted_policy = response.json()['encrypted_policy']
        # derived_key = kdf.derive(shared_key)
        #policy = decrypt_message(encrypted_policy,derived_key)
        return derived_key
    else:
        print("Failed to get shared key")
        return None

if __name__ == "__main__":
    server_public_key = get_server_public_key()
    if server_public_key:
        if login(username, password, server_public_key):
            shared_key = get_shared_key(username, server_public_key)
            if shared_key:
                print("Shared key:", shared_key)
        else:
            print("Login failed")
