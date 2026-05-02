# Spec: Registration

## Overview
Implement user registration so new visitors can create a Spendly account. This step adds the `POST /register` route, a `create_user()` helper in the data layer, and wires up Flask sessions and flash messages. It turns the existing stub `GET /register` (which only renders the form) into a fully functional sign-up flow that validates input, hashes passwords, persists the new user, and redirects on success.

## Depends on
- Step 1 (Database Setup) — `get_db()`, `init_db()`, and the `users` table must exist.

## Routes
- `POST /register` — process registration form, create user, redirect to login — public
- `GET /register` — already implemented (renders `register.html`) — no changes needed to the GET handler

## Database changes
No new tables. One new helper function added to `database/db.py`:

- `create_user(name, email, password)` — hashes password, inserts row into `users`, returns the new `id`. Raises `sqlite3.IntegrityError` on duplicate email.
- `get_user_by_email(email)` — returns a single `users` row or `None`. Needed for duplicate-check feedback before insert.

No schema alterations; the `users` table from Step 1 is sufficient.

## Templates
- **Modify:** `templates/register.html` — add the HTML form (`method="POST"`, `action="{{ url_for('register') }}"`) with fields for `name`, `email`, `password`, `confirm_password`; display flashed error/success messages.

## Files to change
- `app.py` — add `POST /register` route; import `create_user`, `get_user_by_email`; set `app.secret_key`; import `flash`, `redirect`, `request`, `session`, `url_for` from Flask.
- `database/db.py` — add `create_user()` and `get_user_by_email()`.
- `templates/register.html` — add form markup and flash message display.

## Files to create
- `static/css/register.css` — page-specific styles for the registration form (import via `register.html`, not inline `<style>`).

## New dependencies
No new dependencies. `werkzeug.security.generate_password_hash` is already available via Flask's dependency.

## Rules for implementation
- No SQLAlchemy or ORMs — raw `sqlite3` only.
- Parameterised queries only (`?` placeholders) — never f-strings in SQL.
- Passwords hashed with `werkzeug.security.generate_password_hash` — never stored in plaintext.
- Use CSS variables — never hardcode hex values.
- All templates extend `base.html`.
- `app.secret_key` must be set before any session/flash usage; use a hard-coded dev string for now (e.g. `"dev-secret-change-in-prod"`).
- Validate server-side: name non-empty, valid email format (basic check), password ≥ 8 chars, passwords match.
- Use `flash()` for user-facing errors and success messages; display them in `register.html`.
- On duplicate email, catch `sqlite3.IntegrityError` and flash a friendly error — do not let the exception propagate.
- On success, redirect to `url_for('login')` — do not auto-log the user in at this step.
- Use `abort(400)` only for truly malformed requests; use `flash` + re-render for validation errors.

## Definition of done
- [ ] Submitting the form with valid, unique details creates a new row in `users` with a hashed password and redirects to `/login`.
- [ ] Submitting with a blank name, blank email, or blank password re-renders the form with an error message.
- [ ] Submitting with a password shorter than 8 characters shows a validation error.
- [ ] Submitting with mismatched `password` and `confirm_password` shows a validation error.
- [ ] Submitting with an email already in `users` shows "Email already registered" (no stack trace).
- [ ] Password stored in the database is a bcrypt/werkzeug hash, not plaintext.
- [ ] The registration form is accessible at `GET /register` and submits to `POST /register`.
- [ ] All internal links use `url_for()` — no hardcoded paths.
- [ ] `pytest` passes with no errors after implementation.
