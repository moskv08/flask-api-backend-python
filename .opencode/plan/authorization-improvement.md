# Security & API: Input Validation and Authorization

## Problem
Some API endpoints don't properly validate that the authenticated user has access to perform operations on specific resources. Additionally, the API design has some inconsistencies in error handling and response formats.

## Solution
1. Add proper authorization checks in routes to ensure users can only access their own resources
2. Improve input validation consistency across all endpoints
3. Standardize error response formats and HTTP status codes
4. Add comprehensive input validation for all route parameters

## Files to Modify:
1. `backend/routes/todos.py` - Add authorization checks and improve validation
2. `backend/routes/users.py` - Add authorization checks and improve validation
3. `backend/routes/auth.py` - Improve error handling consistency
4. `backend/validation/user_validation.py` - Enhance validation logic

## Implementation Steps:
1. Modify todo routes to verify user ownership before operations (e.g., /users/<int:user_id>/todos)
2. Add proper validation that authenticated user matches the target user in URL paths
3. Standardize error response format across all routes to include consistent error codes and messages
4. Implement comprehensive input validation for all route parameters
5. Ensure proper HTTP status codes (200, 201, 400, 401, 403, 404, 500) are used consistently
6. Add validation for user_id in URL paths to ensure they match the authenticated user context

## Acceptance Criteria:
- All routes properly validate user authorization
- Unauthorized access attempts return 403 or 404 errors appropriately
- User data operations can only be performed on user's own resources
- API behavior is consistent with authorization requirements
- All routes return properly formatted error responses with consistent structure
- Input validation is comprehensive and prevents invalid data from being processed
- HTTP status codes are used consistently across all endpoints