# Spec: Login and Logout

## Overview
Implement session-based login and logout so registered users can authenticate and access protected areas of Spendly. This step adds the `POST /login` route to verify credentials and establish a Flask session, and upgrades the `GET /logout` stub to clear the session and redirect to the landing page. It also fixes the hardcoded `/login` action URL in `login.html` to use `url_for()`, and adds flash-message support to the login form to surface authentication errors.

## Depends on
- Step 1 (Database Setup) — `get_db()`, `init_db()`, and the `users` table must exist.
- Step 2 (Registration) — `get_user_by_email()` and `create_user()` must exist; a user row must be creatable so login can be tested.

## Routes
- `POST /login` — validate credentials, set session, redirect to `/profile` on success — public
- `GET /login` — already implemented (renders `login.html`) — minor fix only (see Templates)
- `GET /logout` — clear session, redirect to `/` — public (currently a stub returning a string)

## Database changes
No database changes. `get_user_by_email(email)` already exists in `database/db.py` and is sufficient for credential lookup. One new helper is needed:

- `verify_user(email, password)` — calls `get_user_by_email()`, checks the password against the stored hash using `werkzeug.security.check_password_hash`, returns the user row on success or `None` on failure.

## Templates
- **Modify:** `templates/login.html`
  - Change `action="/login"` to `action="{{ url_for('login') }}"` (fix hardcoded URL)
  - Replace `{% if error %}` / `{{ error }}` variable rendering with Flask `get_flashed_messages()` so flash messages from the route are displayed consistently with `register.html`

## Files to change
- `app.py` — add `POST /login` route; implement `GET /logout` (replace stub string return); import `session`, `check_password_hash` is not needed in app.py directly (use the new `verify_user` helper); ensure `session` is imported from Flask.
- `database/db.py` — add `verify_user(email, password)` helper.
- `templates/login.html` — fix hardcoded action URL; switch error display to flashed messages.

## Files to create
No new files required.

## New dependencies
No new dependencies. `werkzeug.security.check_password_hash` is already available via Flask's dependency.

## Rules for implementation
- No SQLAlchemy or ORMs — raw `sqlite3` only.
- Parameterised queries only (`?` placeholders) — never f-strings in SQL.
- Passwords verified with `werkzeug.security.check_password_hash` — never compare plaintext.
- Use CSS variables — never hardcode hex values.
- All templates extend `base.html`.
- Store only `user_id` and `user_name` in `session` — never store the password hash or full row.
- Use `flash()` for login errors — do not pass `error=` as a template variable.
- On failed login, re-render `login.html` — do not redirect.
- On successful login, redirect to `url_for('profile')`.
- `GET /logout` must call `session.clear()` then redirect to `url_for('landing')`.
- Do not guard `/logout` with a login check — clearing an already-empty session is harmless.

## Definition of done
- [ ] Submitting valid credentials sets `session['user_id']` and `session['user_name']` and redirects to `/profile`.
- [ ] Submitting an unrecognised email renders `login.html` with a flash error and does not redirect.
- [ ] Submitting a correct email with a wrong password renders `login.html` with a flash error and does not redirect.
- [ ] Submitting with blank email or blank password renders `login.html` with a flash error.
- [ ] Visiting `/logout` clears the session and redirects to `/`.
- [ ] After logout, `session['user_id']` is no longer present.
- [ ] The login form `action` uses `url_for('login')` — no hardcoded URL.
- [ ] `pytest` passes with no errors after implementation.
