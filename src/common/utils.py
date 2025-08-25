import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from datetime import datetime
import sys


def is_unittest():
    if 'unittest' in sys.modules.keys():
        return True
    return False


def generate_key(seed):
    seed_bytes = seed.encode('utf-32')
    salt = b'salt_value_for_asyncio_by_example'
    iterations = 100000 
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    key = kdf.derive(seed_bytes)
    return key


def encrypt(text, key):
    """
        Encryption function
    """
    cipher_suite = Fernet(key)
    return cipher_suite.encrypt(text.encode())


def decrypt(text, key):
    """
        Decryption function
    """
    cipher_suite = Fernet(key)
    return cipher_suite.decrypt(text).decode()


def test_generate_key(texto="ApplicacionPPTools"):
    bytes_texto = generate_key(texto)
    key = bytes_texto
    key_base64 = base64.urlsafe_b64encode(key)
    mensaje = "hola mundo"
    encrypted = encrypt(mensaje, key_base64)
    decrypted = decrypt(encrypted, key_base64)
    assert mensaje == decrypted


def get_encryption_key(texto="ApplicacionPPTools"):
    bytes_texto = generate_key(texto)
    key = bytes_texto
    key_base64 = base64.urlsafe_b64encode(key)
    return key_base64


def generate_timestamp_pattern(basename, prefix=None, timestamp_format="%Y_%m_%d", extension=None):
    now = datetime.now()
    sufix = now.strftime(timestamp_format)
    pattern_filename = "{0}_{1}".format(basename, sufix)
    if prefix:
        pattern_filename = prefix + "_" + pattern_filename
    if extension:
        pattern_filename = pattern_filename + "." + extension
    return pattern_filename