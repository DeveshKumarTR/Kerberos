"""
Cryptographic Utilities for Kerberos Authentication
Author: Devesh Kumar
Description: Encryption, decryption, and key generation utilities
"""

import os
import base64
import hashlib
import secrets
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from typing import Optional


class CryptoUtils:
    """
    Cryptographic utilities for Kerberos authentication
    """
    
    def __init__(self):
        self.salt = os.getenv('CRYPTO_SALT', 'kerberos-salt').encode('utf-8')
        self.backend = default_backend()
        self._fernet_key = self._derive_key()
        self.fernet = Fernet(self._fernet_key)
    
    def _derive_key(self) -> bytes:
        """
        Derive encryption key from password and salt
        """
        password = os.getenv('CRYPTO_PASSWORD', 'kerberos-password').encode('utf-8')
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=self.backend
        )
        
        key = kdf.derive(password)
        return base64.urlsafe_b64encode(key)
    
    def encrypt_data(self, data: str) -> bytes:
        """
        Encrypt string data using Fernet symmetric encryption
        """
        try:
            return self.fernet.encrypt(data.encode('utf-8'))
        except Exception as e:
            print(f"Encryption error: {str(e)}")
            raise
    
    def decrypt_data(self, encrypted_data: bytes) -> str:
        """
        Decrypt data using Fernet symmetric encryption
        """
        try:
            decrypted_bytes = self.fernet.decrypt(encrypted_data)
            return decrypted_bytes.decode('utf-8')
        except Exception as e:
            print(f"Decryption error: {str(e)}")
            raise
    
    def generate_session_key(self) -> str:
        """
        Generate a random session key
        """
        return secrets.token_urlsafe(32)
    
    def generate_random_bytes(self, length: int = 32) -> bytes:
        """
        Generate cryptographically secure random bytes
        """
        return secrets.token_bytes(length)
    
    def hash_password(self, password: str, salt: Optional[bytes] = None) -> tuple[bytes, bytes]:
        """
        Hash a password with salt using PBKDF2
        """
        if salt is None:
            salt = secrets.token_bytes(32)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=self.backend
        )
        
        password_hash = kdf.derive(password.encode('utf-8'))
        return password_hash, salt
    
    def verify_password(self, password: str, password_hash: bytes, salt: bytes) -> bool:
        """
        Verify a password against its hash
        """
        try:
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=self.backend
            )
            
            kdf.verify(password.encode('utf-8'), password_hash)
            return True
        except Exception:
            return False
    
    def generate_nonce(self) -> str:
        """
        Generate a cryptographic nonce
        """
        return secrets.token_hex(16)
    
    def compute_hmac(self, data: str, key: str) -> str:
        """
        Compute HMAC-SHA256 of data with key
        """
        import hmac
        
        hmac_obj = hmac.new(
            key.encode('utf-8'),
            data.encode('utf-8'),
            hashlib.sha256
        )
        
        return hmac_obj.hexdigest()
    
    def verify_hmac(self, data: str, key: str, expected_hmac: str) -> bool:
        """
        Verify HMAC-SHA256 of data
        """
        import hmac
        computed_hmac = self.compute_hmac(data, key)
        return hmac.compare_digest(computed_hmac, expected_hmac)
    
    def aes_encrypt(self, plaintext: str, key: bytes) -> tuple[bytes, bytes]:
        """
        Encrypt data using AES-256-CBC
        """
        try:
            # Generate random IV
            iv = secrets.token_bytes(16)
            
            # Pad plaintext to multiple of 16 bytes
            padded_plaintext = self._pad_data(plaintext.encode('utf-8'))
            
            # Create cipher
            cipher = Cipher(
                algorithms.AES(key),
                modes.CBC(iv),
                backend=self.backend
            )
            
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
            
            return ciphertext, iv
            
        except Exception as e:
            print(f"AES encryption error: {str(e)}")
            raise
    
    def aes_decrypt(self, ciphertext: bytes, key: bytes, iv: bytes) -> str:
        """
        Decrypt data using AES-256-CBC
        """
        try:
            # Create cipher
            cipher = Cipher(
                algorithms.AES(key),
                modes.CBC(iv),
                backend=self.backend
            )
            
            decryptor = cipher.decryptor()
            padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            
            # Remove padding
            plaintext = self._unpad_data(padded_plaintext)
            
            return plaintext.decode('utf-8')
            
        except Exception as e:
            print(f"AES decryption error: {str(e)}")
            raise
    
    def _pad_data(self, data: bytes) -> bytes:
        """
        Apply PKCS7 padding
        """
        padding_length = 16 - (len(data) % 16)
        padding = bytes([padding_length] * padding_length)
        return data + padding
    
    def _unpad_data(self, padded_data: bytes) -> bytes:
        """
        Remove PKCS7 padding
        """
        padding_length = padded_data[-1]
        return padded_data[:-padding_length]
    
    def generate_aes_key(self) -> bytes:
        """
        Generate a 256-bit AES key
        """
        return secrets.token_bytes(32)
    
    def encode_base64(self, data: bytes) -> str:
        """
        Encode bytes to base64 string
        """
        return base64.b64encode(data).decode('utf-8')
    
    def decode_base64(self, data: str) -> bytes:
        """
        Decode base64 string to bytes
        """
        return base64.b64decode(data.encode('utf-8'))
    
    def hash_sha256(self, data: str) -> str:
        """
        Compute SHA-256 hash of data
        """
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
    
    def secure_compare(self, a: str, b: str) -> bool:
        """
        Constant-time string comparison
        """
        import hmac
        return hmac.compare_digest(a, b)
