# Security: Secret Key Configuration

## Problem
The SECRET_KEY in config.py has a fallback to 'dev-secret-key', which is insecure for production environments and could lead to predictable JWT tokens.

## Solution
1. Remove the fallback SECRET_KEY in config.py
2. Ensure SECRET_KEY is required to be set via environment variables
3. Add documentation about secret key configuration

## Files to Modify:
1. `backend/config.py` - Remove fallback SECRET_KEY
2. `backend/README.md` - Add documentation for secret key setup

## Implementation Steps:
1. Modify config.py to remove the fallback SECRET_KEY
2. Update documentation in README.md about proper secret key configuration
3. Add validation to ensure SECRET_KEY is set

## Acceptance Criteria:
- SECRET_KEY can no longer fall back to 'dev-secret-key'
- Application fails to start if SECRET_KEY is not set
- Documentation clearly explains how to configure SECRET_KEY properly