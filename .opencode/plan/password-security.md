# Security: Password Hashing Implementation

## Problem
The current authentication implementation stores passwords in plain text, which is a critical security vulnerability. Passwords should be hashed using a secure hashing algorithm like bcrypt.

## Solution
1. Add bcrypt dependency to pyproject.toml
2. Implement password hashing in the authentication flow
3. Update the login method to verify hashed passwords
4. Create a utility function for password hashing and verification

## Files to Modify:
1. `backend/pyproject.toml` - Add bcrypt dependency
2. `backend/routes/auth.py` - Update password handling logic

## Implementation Steps:
1. Add bcrypt to dependencies in pyproject.toml
2. Import bcrypt in auth.py
3. Modify the login function to verify hashed passwords instead of plain text
4. Add password hashing utility functions
5. Update the user creation to hash passwords when provided

## Acceptance Criteria:
- Passwords are never stored in plain text
- Login functionality works with hashed passwords
- User creation properly hashes passwords