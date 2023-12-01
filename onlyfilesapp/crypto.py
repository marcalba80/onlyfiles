from django.core.files.base import ContentFile

import secrets
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def generate_master_key_repository():
    key = secrets.token_bytes(32)
    return key.hex()

def derive_key(master_key, salt, info):
    kdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        info=info,
        backend=default_backend()
    )
    return kdf.derive(bytes.fromhex(master_key))

def encrypt_file(master_key, salt, info, file):

    file.seek(0)
    plaintext = file.read()

    key = derive_key(master_key, salt, info)

    iv = hashes.Hash(hashes.SHA256(), backend=default_backend())
    iv.update(info)
    iv = iv.finalize()[:16]

    cipher = Cipher(algorithms.AES(key), modes.GCM(initialization_vector=iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    file.close()

    encrypted_file = ContentFile(ciphertext)

    return encrypted_file, encryptor.tag.hex()

def decrypt_file(master_key, salt, info, tag, file):

    file.seek(0)
    ciphertext = file.read()

    key = derive_key(master_key, salt, info)

    iv = hashes.Hash(hashes.SHA256(), backend=default_backend())
    iv.update(info)
    iv = iv.finalize()[:16]

    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, bytes.fromhex(tag)))
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    file.close()

    decrypted_file = ContentFile(plaintext)

    return decrypted_file
