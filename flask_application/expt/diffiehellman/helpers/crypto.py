from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def generate_dh_key_pair():
    # Generate private and public key for Diffie-Hellman
    parameters = dh.generate_parameters(generator=2, key_size=2048)
    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()

    return private_key, public_key

def perform_dh_key_exchange(private_key, other_party_public_key):
    # Perform key exchange with the other party's public key
    shared_key = private_key.exchange(other_party_public_key)
    return shared_key

def encrypt_message(message, key):
    # Generate a random initialization vector (IV)
    iv = os.urandom(16)  # 16 bytes IV for AES

    # Create a Cipher object with AES CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad the message to be a multiple of 16 bytes (AES block size)
    if len(message) % 16 != 0:
        message += b' ' * (16 - len(message) % 16)

    # Encrypt the padded message
    encrypted_message = encryptor.update(message) + encryptor.finalize()

    # Return the IV along with the encrypted message
    return iv + encrypted_message

def decrypt_message(encrypted_message, key, iv):
    # Create a Cipher object with AES CBC mode and the provided IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the encrypted message
    decrypted_message = decryptor.update(encrypted_message) + decryptor.finalize()

    return decrypted_message

if __name__ == "__main__":
    # Alice generates her key pair
    alice_private_key, alice_public_key = generate_dh_key_pair()

    # Bob generates his key pair
    bob_private_key, bob_public_key = generate_dh_key_pair()

    # Alice performs key exchange with Bob's public key
    alice_shared_key = perform_dh_key_exchange(alice_private_key, bob_public_key)

    # Bob performs key exchange with Alice's public key
    bob_shared_key = perform_dh_key_exchange(bob_private_key, alice_public_key)

    # Check if Alice and Bob have the same shared key
    assert alice_shared_key == bob_shared_key

    # Encrypt a message using the shared key
    message = b"Hello, this is a secret message."
    encrypted_message = encrypt_message(message, alice_shared_key)

    # Decrypt the encrypted message using the shared key
    decrypted_message = decrypt_message(encrypted_message[16:], alice_shared_key, encrypted_message[:16])

    print("Original message:", message.decode())
    print("Decrypted message:", decrypted_message.decode())
