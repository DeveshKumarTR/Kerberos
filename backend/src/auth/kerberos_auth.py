"""
Kerberos Authentication Implementation
Author: Devesh Kumar
Description: Three-headed authentication system (AS, TGS, SS)
"""

import json
import time
import base64
import hashlib
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import bcrypt
from typing import Optional, Dict, Any

from ..models.user import User
from ..utils.crypto_utils import CryptoUtils


class KerberosAuth:
    """
    Kerberos Authentication System
    Implements the three-headed dog approach:
    1. Authentication Server (AS)
    2. Ticket Granting Server (TGS) 
    3. Service Server (SS)
    """
    
    def __init__(self):
        self.secret_key = os.getenv('KERBEROS_SECRET', 'kerberos-secret-key')
        self.crypto_utils = CryptoUtils()
        self.tgt_lifetime = timedelta(hours=8)
        self.service_ticket_lifetime = timedelta(hours=2)
        
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Phase 1: Authentication Server (AS) - First head of Cerberus
        Validates user credentials against the database
        """
        try:
            # In a real implementation, this would query a database
            # For demo purposes, we'll use a simple user store
            user = self._get_user_by_username(username)
            
            if user and self._verify_password(password, user.password_hash):
                return user
            
            return None
            
        except Exception as e:
            print(f"Authentication error: {str(e)}")
            return None
    
    def generate_tgt(self, user_id: str, username: str) -> str:
        """
        Phase 2: Ticket Granting Server (TGS) - Second head of Cerberus
        Generates a Ticket Granting Ticket (TGT)
        """
        try:
            tgt_data = {
                'user_id': user_id,
                'username': username,
                'issued_at': datetime.now().isoformat(),
                'expires_at': (datetime.now() + self.tgt_lifetime).isoformat(),
                'session_key': self.crypto_utils.generate_session_key(),
                'permissions': ['read', 'write', 'execute']
            }
            
            # Encrypt TGT data
            encrypted_tgt = self.crypto_utils.encrypt_data(json.dumps(tgt_data))
            
            return base64.b64encode(encrypted_tgt).decode('utf-8')
            
        except Exception as e:
            print(f"TGT generation error: {str(e)}")
            raise
    
    def generate_service_ticket(self, tgt: str, service_name: str) -> str:
        """
        Phase 3: Service Server (SS) - Third head of Cerberus
        Generates a service ticket for accessing specific resources
        """
        try:
            # Validate TGT first
            tgt_data = self._validate_tgt(tgt)
            if not tgt_data:
                raise ValueError("Invalid TGT")
            
            service_ticket_data = {
                'user_id': tgt_data['user_id'],
                'username': tgt_data['username'],
                'service_name': service_name,
                'issued_at': datetime.now().isoformat(),
                'expires_at': (datetime.now() + self.service_ticket_lifetime).isoformat(),
                'session_key': self.crypto_utils.generate_session_key(),
                'permissions': tgt_data.get('permissions', [])
            }
            
            # Encrypt service ticket
            encrypted_ticket = self.crypto_utils.encrypt_data(json.dumps(service_ticket_data))
            
            return base64.b64encode(encrypted_ticket).decode('utf-8')
            
        except Exception as e:
            print(f"Service ticket generation error: {str(e)}")
            raise
    
    def validate_service_ticket(self, service_ticket: str) -> bool:
        """
        Validates a service ticket for resource access
        """
        try:
            # Decode and decrypt service ticket
            encrypted_data = base64.b64decode(service_ticket.encode('utf-8'))
            decrypted_data = self.crypto_utils.decrypt_data(encrypted_data)
            ticket_data = json.loads(decrypted_data)
            
            # Check expiration
            expires_at = datetime.fromisoformat(ticket_data['expires_at'])
            if datetime.now() > expires_at:
                return False
            
            return True
            
        except Exception as e:
            print(f"Service ticket validation error: {str(e)}")
            return False
    
    def _validate_tgt(self, tgt: str) -> Optional[Dict[str, Any]]:
        """
        Internal method to validate TGT
        """
        try:
            # Decode and decrypt TGT
            encrypted_data = base64.b64decode(tgt.encode('utf-8'))
            decrypted_data = self.crypto_utils.decrypt_data(encrypted_data)
            tgt_data = json.loads(decrypted_data)
            
            # Check expiration
            expires_at = datetime.fromisoformat(tgt_data['expires_at'])
            if datetime.now() > expires_at:
                return None
            
            return tgt_data
            
        except Exception as e:
            print(f"TGT validation error: {str(e)}")
            return None
    
    def _get_user_by_username(self, username: str) -> Optional[User]:
        """
        Retrieve user from database (mock implementation)
        In production, this would query the actual database
        """
        # Mock users for demonstration
        mock_users = {
            'admin': User(
                id='1',
                username='admin',
                password_hash=bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()),
                roles=['admin', 'user']
            ),
            'user': User(
                id='2',
                username='user',
                password_hash=bcrypt.hashpw('user123'.encode('utf-8'), bcrypt.gensalt()),
                roles=['user']
            ),
            'guest': User(
                id='3',
                username='guest',
                password_hash=bcrypt.hashpw('guest123'.encode('utf-8'), bcrypt.gensalt()),
                roles=['guest']
            )
        }
        
        return mock_users.get(username)
    
    def _verify_password(self, password: str, password_hash: bytes) -> bool:
        """
        Verify password against hash
        """
        try:
            return bcrypt.checkpw(password.encode('utf-8'), password_hash)
        except Exception as e:
            print(f"Password verification error: {str(e)}")
            return False
    
    def get_ticket_info(self, ticket: str) -> Optional[Dict[str, Any]]:
        """
        Extract information from a ticket without validating it
        """
        try:
            encrypted_data = base64.b64decode(ticket.encode('utf-8'))
            decrypted_data = self.crypto_utils.decrypt_data(encrypted_data)
            ticket_data = json.loads(decrypted_data)
            
            return {
                'username': ticket_data.get('username'),
                'service_name': ticket_data.get('service_name'),
                'issued_at': ticket_data.get('issued_at'),
                'expires_at': ticket_data.get('expires_at'),
                'permissions': ticket_data.get('permissions', [])
            }
            
        except Exception as e:
            print(f"Ticket info extraction error: {str(e)}")
            return None
