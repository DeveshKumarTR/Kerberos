"""
User Model
Author: Devesh Kumar
Description: User data model for Kerberos authentication
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import json


class User:
    """
    User model for Kerberos authentication system
    """
    
    def __init__(self, id: str, username: str, password_hash: bytes, roles: Optional[List[str]] = None):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.roles = roles or ['user']
        self.created_at = datetime.now()
        self.last_login = None
        self.login_count = 0
        self.is_active = True
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert user object to dictionary
        """
        return {
            'id': self.id,
            'username': self.username,
            'roles': self.roles,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'login_count': self.login_count,
            'is_active': self.is_active
        }
    
    def to_json(self) -> str:
        """
        Convert user object to JSON string
        """
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """
        Create user object from dictionary
        """
        user = cls(
            id=data['id'],
            username=data['username'],
            password_hash=data['password_hash'],
            roles=data.get('roles', ['user'])
        )
        
        if 'created_at' in data and data['created_at']:
            user.created_at = datetime.fromisoformat(data['created_at'])
        
        if 'last_login' in data and data['last_login']:
            user.last_login = datetime.fromisoformat(data['last_login'])
        
        user.login_count = data.get('login_count', 0)
        user.is_active = data.get('is_active', True)
        
        return user
    
    def update_login(self):
        """
        Update login information
        """
        self.last_login = datetime.now()
        self.login_count += 1
    
    def has_role(self, role: str) -> bool:
        """
        Check if user has a specific role
        """
        return role in self.roles
    
    def add_role(self, role: str):
        """
        Add a role to the user
        """
        if role not in self.roles:
            self.roles.append(role)
    
    def remove_role(self, role: str):
        """
        Remove a role from the user
        """
        if role in self.roles:
            self.roles.remove(role)
    
    def is_admin(self) -> bool:
        """
        Check if user is an admin
        """
        return self.has_role('admin')
    
    def __str__(self) -> str:
        return f"User(id={self.id}, username={self.username}, roles={self.roles})"
    
    def __repr__(self) -> str:
        return self.__str__()
