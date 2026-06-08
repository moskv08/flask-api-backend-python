# JWT Token Blacklisting Implementation Notes

## Current State
The logout functionality in auth.py is incomplete and needs proper token invalidation.

## Implementation Plan

### Phase 1: Update auth.py to support logout with proper token handling
- Keep the current login functionality as-is
- Update logout endpoint to properly handle token invalidation

### Phase 2: Database Integration (Optional but Recommended)
To make logout truly effective, we need to:
1. Create a TokenBlocklist table in the database
2. Configure JWTManager to check for blacklisted tokens
3. Add tokens to blocklist on logout

### Phase 3: JWT Manager Configuration
Add the following to app.py:

```python
from models.token_blocklist import TokenBlocklist

# Configure JWT Manager with token blocklist loader
jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None
```

### Phase 4: Database Migration (Optional)
Create migration to add token_blocklist table:
```bash
alembic revision --autogenerate -m "Add token blocklist table"
```

## Current Implementation Limitation
The current implementation in auth.py only returns a success message on logout but doesn't actually invalidate tokens because:
1. The TokenBlocklist model was causing import issues
2. Database configuration isn't set up for token blacklisting

## Recommendation
For a production system, implement the complete database-based token blacklisting as outlined in the phases above.