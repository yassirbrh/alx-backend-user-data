#!/usr/bin/env python3
'''
	Module for handling authentication system.
'''
import bcrypt


def _hash_password(password: str) -> bytes:
	'''
		_hash_password: function
		@password: Password to encrypt.
		return: the hashed password.
	'''
	return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
