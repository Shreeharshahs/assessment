import hashlib
import os

def generate_salt():
    return os.urandom(16).hex()

def hash_password(password, salt):
    return hashlib.pbkdf2_hmac(
        'sha256',
        password.encode(),
        bytes.fromhex(salt),
        100000
    ).hex()

def verify_password(password, salt, stored_hash):
    return hash_password(password, salt) == stored_hash

def calculate_new_marks(existing_marks, new_marks):
    return existing_marks + new_marks
