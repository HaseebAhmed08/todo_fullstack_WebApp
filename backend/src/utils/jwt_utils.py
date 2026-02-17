"""
JWT utilities module for backward compatibility.
This module exists to support existing test imports.
"""
from .security import create_access_token, decode_access_token, verify_password, get_password_hash

__all__ = ["create_access_token", "decode_access_token", "verify_password", "get_password_hash"]