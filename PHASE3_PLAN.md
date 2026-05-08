# Phase 3 Project Plan: Security Hardening & Multi-User Support

## 1. Goal
Transition the Password Manager from a local single-user prototype to a secure, multi-user application with robust encryption key management and session security.

## 2. Core Security Pillars
- **Zero-Knowledge Architecture:** The server should never store the master password. Decryption keys must be derived on the fly.
- **Key Derivation:** Implement Argon2 or PBKDF2 for deriving the encryption key from a user's master password.
- **Secure Sessions:** Use JWT (JSON Web Tokens) with short TTLs for API authentication.

## 3. Planned Features

### 3.1 Backend: Authentication & User Management
- [ ] **User Registration:** Create a `users` table with fields for `username`, `password_hash` (using Argon2), and `salt`.
- [ ] **Auth Service:** Implement `/api/v1/auth/login` and `/api/v1/auth/register`.
- [ ] **JWT Integration:** Protect all `/api/v1/vaults/**` routes with a `token_required` decorator.

### 3.2 Backend: Encryption Hardening
- [ ] **Dynamic CryptoService:** Modify `CryptoService` to accept a key derived from the user's login session rather than generating a static one.
- [ ] **Master Password Change:** Implement logic to re-encrypt all vault data when a user changes their master password.

### 3.3 Frontend: Security UX
- [ ] **Login Screen:** Implement a login/registration view that precedes the vault management UI.
- [ ] **Sensitive Data Masking:** Add "Show/Hide" toggles for passwords in the UI.
- [ ] **Automatic Logout:** Implement a timer to clear local session data after inactivity.

### 3.4 Infrastructure & Operations
- [ ] **Environment Variables:** Migrate database paths and JWT secrets to a `.env` file (managed by `python-dotenv`).
- [ ] **Audit Logging:** Implement logging for sensitive actions (failed logins, vault deletions).

## 4. Technical Debt & Modernization
- [ ] **FastAPI Migration (Optional/Recommended):** Consider migrating from Flask to FastAPI for better async support and native dependency injection for Auth.
- [ ] **Frontend Refactor:** Transition from Vanilla JS to a lightweight component-based structure if complexity increases.

## 5. Timeline & Milestones
- **Milestone 1:** User Auth & JWT Protection (3 turns)
- **Milestone 2:** Key Derivation & Re-encryption (3 turns)
- **Milestone 3:** UI Hardening & Session UX (2 turns)
- **Milestone 4:** Final Security Audit & 100% Coverage (2 turns)
