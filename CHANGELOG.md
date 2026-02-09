# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-02-08

### Added
- Due date functionality to todos with ISO date format support
- Priority levels (low, medium, high) for todos
- Validation for priority values
- Date format handling in todo updates

### Changed
- Updated Todo model to include due_date and priority fields
- Enhanced todo service with due date and priority handling
- Improved error handling in todos routes

### Fixed
- Completed the todos routes implementation that was previously incomplete
- Added proper validation for date and priority inputs

### Security
- Added input validation to prevent invalid date formats and priority values

## [1.0.0] - 2025-10-06

### Added
- Initial project structure with Flask API
- Basic todo CRUD functionality
- User authentication system with JWT
- Database models for users and todos

### Changed
- Project architecture to separate services, models, and routes

[1.1.0]: https://github.com/your-repo/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/your-repo/commits/v1.0.0