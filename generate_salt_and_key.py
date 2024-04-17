import base64
import os

from cryptography.fernet import Fernet

key = base64.urlsafe_b64encode(Fernet.generate_key())
salt = base64.urlsafe_b64encode(os.urandom(16))
print(f'key: {key}')
print(f'salt: {salt}')
