# Performance: Database Indexes

## Problem
The todos table lacks indexes on the user_id column, which will cause performance issues as the database grows.

## Solution
1. Add indexes to the todos table for user_id column
2. Update Alembic migration files to include these indexes

## Files to Modify:
1. `backend/models/todo.py` - Add index to user_id column
2. `backend/alembic/versions/07f5c00d1485_add_date_and_priorit_fields_to_todo_.py` - Add index to migration

## Implementation Steps:
1. Modify the User model to add indexes on user_id columns in todos table
2. Update Alembic migration to include the index creation
3. Test that indexes are properly applied

## Acceptance Criteria:
- user_id column in todos table has an index
- Database queries on todos by user_id are optimized
- Alembic migrations properly handle the new index