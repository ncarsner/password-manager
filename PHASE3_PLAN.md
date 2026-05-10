# Phase 3 Project Plan: Security Hardening & Multi-User Support

## 1. Goal
Transition the Password Manager from a local single-user prototype to a secure, multi-user application with robust encryption key management and session security.

## 2. Core Security Pillars
- **Zero-Knowledge Architecture:** The server should never store the master password. Decryption keys must be derived on the fly.
- **Key Derivation:** Implement Argon2 or PBKDF2 for deriving the encryption key from a user's master password.
- **Secure Sessions:** Use JWT (JSON Web Tokens) with short TTLs for API authentication.

---

## 3. Current State (as of revision-v2)

### Completed before Phase 3
- [x] **Persistent Fernet key** — `_load_or_create_fernet_key()` in `config.py` writes to `.env` on first run; survives restarts. Equivalent to a server-side pepper.
- [x] **Environment variables** — `.env` + `python-dotenv` for `FERNET_KEY`, `DATABASE_PATH`, `SECRET_KEY`, `DEBUG`.
- [x] **Password length validation** — 8–32 chars enforced in API (`v1.py`) and HTML (`minlength`/`maxlength`).
- [x] **Decrypt failure handling** — Returns `null` password field; UI shows red "Unrecoverable — delete and re-add".
- [x] **Credential table UI** — `table-layout: fixed`, columnar (Domain | Username | Password | Notes | Delete), stable widths.
- [x] **Show/Hide toggle** — Color-coded (blue = hidden, orange = visible).
- [x] **Copy button** — Copies plaintext without requiring Show; grey → green feedback.
- [x] **100% test coverage** — 20 tests across `test_api.py` + `test_units.py`.

### Not yet started (Phase 3 scope)
- [ ] Credential edit/update (PATCH endpoint + inline UI) — **immediate next task**
- [ ] User registration and login
- [ ] Argon2 password hashing for stored user credentials
- [ ] JWT-protected routes
- [ ] Per-user key derivation from master password
- [ ] Master password change with re-encryption
- [ ] Login/registration frontend view
- [ ] Automatic session logout on inactivity
- [ ] Audit logging (failed logins, vault deletions)

---

## 4. Planned Features

### 4.1 Credential Edit (Immediate — Pre-Auth)
Implement inline edit for stored credentials without delete-and-re-add:
- [ ] **Backend:** `PATCH /api/v1/passwords/<id>` — accepts partial updates to `domain`, `username`, `password`, `notes`. Re-encrypts password with current Fernet key if provided. Validates 8–32 chars if password supplied.
- [ ] **Storage:** `update_password()` method in `StorageService`.
- [ ] **Frontend:** Edit button per row → inline form or row-level edit mode → Save/Cancel.
- [ ] **Tests:** Cover partial update, password re-encrypt, validation, not-found.

### 4.2 Backend: Authentication & User Management
- [ ] **`users` table:** `id`, `username` (unique), `password_hash` (Argon2), `salt`.
- [ ] **Auth service:** `POST /api/v1/auth/register`, `POST /api/v1/auth/login` → returns JWT.
- [ ] **JWT middleware:** `token_required` decorator protecting all `/api/v1/vaults/**` and `/api/v1/passwords/**` routes.
- [ ] **User-scoped vaults:** `vaults` table gains `user_id` FK; queries filter by authenticated user.

### 4.3 Backend: Encryption Hardening
- [ ] **Per-user key derivation:** On login, derive Fernet key from master password + stored salt using Argon2. Current server-wide `FERNET_KEY` replaced with session-derived keys.
- [ ] **Master password change:** Re-encrypt all vault data atomically; old key discarded only after success.

### 4.4 Frontend: Security UX
- [ ] **Login/register screen:** Precedes vault management; stores JWT in `sessionStorage` (not `localStorage`).
- [ ] **Automatic logout:** Clear session after configurable inactivity timeout.
- [ ] **Auth headers:** All API calls include `Authorization: Bearer <token>`.

### 4.5 Infrastructure
- [ ] **Audit logging:** Structured log entries for failed logins, vault deletions, password changes.

---

## 5. Technical Debt / Modernization (Optional)
- [ ] **FastAPI migration:** Better async support and native dependency injection for auth middleware. Low priority unless auth complexity grows.
- [ ] **Frontend component refactor:** Vanilla JS → lightweight component structure if login/auth flow grows complex.

---

## 6. Timeline & Milestones

| Milestone | Scope | Est. turns |
|-----------|-------|------------|
| **M0** | Credential edit (PATCH + UI) | 1 |
| **M1** | User auth & JWT protection | 3 |
| **M2** | Per-user key derivation & re-encryption | 3 |
| **M3** | UI hardening & session UX | 2 |
| **M4** | Final security audit & 100% coverage | 2 |
