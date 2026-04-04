# Project Roadmap

This document outlines the strategic evolution of the Todo API, organized by architectural milestones.

## 🎯 Current Focus: Phase 2 (Identity & Security)
*Goal: Transition from a public CRUD API to a secure, user-centric service.*

### 🛠️ Active Tasks
- [x] **Authentication:** Implement full login/logout flow.
- [x] **Ownership:** Restrict Todo access to specific users (User-specific lists).
- [ ] **Security Hardening:** 
    - [ ] Add CSRF protection.
    - [ ] Implement Rate Limiting to prevent abuse.
    - [ ] Implement Input Sanitization.
- [x] **Feature Expansion:** Add due dates and priority levels to todos.

---

## 🗺️ Future Milestones

### Phase 3: Production Readiness & Observability 🛡️
*Goal: Prepare the application for deployment in a stable, monitorable environment.*

### 🏗️ Infrastructure & Deployment
- [ ] **Database:** Migrate from local SQLite to PostgreSQL.
- [ ] **Containerization:** Create Dockerfile and orchestration setup.
    - [ ] Add CI/CD pipeline configuration.
- [ ] **Server Configuration:** Set up Gunicorn (WSGI) and SSL certificates.
- [ ] **Environment Management:** Standardize `.env` variable configuration.

### 🔍 Observability & Documentation
- [ ] **Logging:** Implement structured logging configuration.
- [ ] **API Docs:** Create full Swagger/OpenAPI documentation.
- [ ] **Testing:** Achieve high coverage with Unit and Integration tests.
- [ ] **Error Management:** Implement standardized, user-friendly error pages/responses.

### Phase 4: Scalability & Advanced Features 🚀
*Goal: Optimize performance for large datasets and introduce complex functionality.*

### 📈 Performance & Scaling
- [ ] **Pagination:** Implement pagination for large todo lists.
- [ ] **Search & Filter:** Enhance search capabilities and add status filtering (completed/pending).
- [ ] **Efficiency:** Implement caching strategies for frequently accessed data.

### ✨ Advanced User Experience
- [ ] **Real-time:** Implement WebSockets for live updates.
- [ ] **Organization:** Add Todo categories, tags, and recurring tasks.
- [ ] **Interactivity:** Implement todo sharing between users.
- [ ] **Data Portability:** Create export functionality (CSV/PDF).
- [ ] **Notifications:** Add reminders via Email or SMS.

---

## 🛠️ Tooling & Experimentation
*Non-product related tasks, integrations, and research.*
- [ ] Integrate Brave MCP with LM Studio.