# Advanced Tasks

These tasks are for experienced participants or participants who finish early. The goal is not to make an attack succeed. The goal is to change a vulnerable implementation into a safer one and confirm that the same attack steps no longer work.

## How to Work

1. Reproduce the behavior while the app is vulnerable.
2. Change the minimum amount of code.
3. Try the same input again.
4. Explain why the attack now fails.
5. Check for side effects in normal app behavior.

Each task can be done independently. If multiple people work in parallel, divide ownership by file and feature.

## Task A: Prevent SQL Injection

Target:

- `/login` in `app/main.py`

Current vulnerable code:

```python
sql = "SELECT * FROM users WHERE username='" + username + "' and password='" + password + "';"
records = cursor.execute(sql)
```

Do:

- Stop concatenating values into SQL strings.
- Use placeholders.
- Confirm failed login does not crash the app.

Acceptance criteria:

- `koide` / `password` logs in.
- `koide` / `' or 'a'='a` does not log in.
- `koide' --` / `anything` does not log in.
- SQL or messages shown on screen do not mislead students.

Hint:

```python
records = cursor.execute(
    "SELECT * FROM users WHERE username=? and password=?;",
    (username, password),
)
```

## Task B: Prevent XSS

Target:

- `app/views/bbs.tpl`

Current vulnerable code:

```html
{{!comment.comment}}
```

Do:

- Enable escaping when displaying comments.
- Confirm posted content is displayed as text.
- Confirm normal BBS posts still work.

Acceptance criteria:

- Posting `<script>alert(1)</script>` does not execute JavaScript.
- The post appears as text in the list.
- Existing comments are still displayed.

Hint:

```html
{{comment.comment}}
```

## Task C: Add Cookie Attributes

Target:

- `/login` in `app/main.py`

Do:

- Add attributes to `response.set_cookie()`.
- Confirm login state using `/cookies`.
- Observe how the XSS exercise result changes.

Acceptance criteria:

- Login works.
- `/mypage` and `/bbs` work.
- The cookie sets `HttpOnly` and `SameSite`.
- You can explain whether JavaScript can read `cookie_id`.

Hint:

```python
response.set_cookie(
    "cookie_id",
    cookie_id,
    secret=COOKIE_SECRET,
    httponly=True,
    samesite="Lax",
)
```

Note:

- `Secure=True` assumes HTTPS. In this local HTTP exercise, setting it may prevent the cookie from being sent.

## Task D: Implement CSRF Tokens

Targets:

- `/bbs` in `app/main.py`
- `app/views/bbs.tpl`

Do:

- Give each logged-in user an unpredictable CSRF token.
- Embed the token in the form.
- Verify the token on POST.
- Remove the fixed token behavior.

Acceptance criteria:

- A legitimate post from the BBS page succeeds.
- A post from `http://localhost:8090/csrf` fails.
- Failure shows a clear error.

Hint:

```python
import secrets

def ensure_csrf_token(user):
    if not user.session:
        user.session = secrets.token_urlsafe(32)
        user.save()
    return user.session
```

On POST:

```python
token = request.forms.decode().get("token", "")
if not user.session or token != user.session:
    return error_page("CSRF token is invalid.", status=403)
```

## Task E: Prevent Command Injection

Target:

- `/contact` in `app/main.py`

Current vulnerable code:

```python
command = f'/bin/echo "From: {address}\n{comment}" >> "{OUTBOX_FILE}"'
exit_code = os.system(command)
```

Do:

- Stop using `os.system()`.
- Save contact messages without going through a shell.
- Keep the contact form behavior.

Acceptance criteria:

- Normal contact submission works.
- Entering `"; /bin/echo injected > command_injection_result.txt; #` does not create the file.
- The submitted input remains as text in the stored message.

Hint:

```python
with OUTBOX_FILE.open("a", encoding="utf-8") as outbox:
    outbox.write(f"From: {address}\n{comment}\n---\n")
```

## Task F: Hash Passwords

Targets:

- `Users.password`
- `/register`
- `/login`
- `initialize_database()`

Do:

- Stop storing plain-text passwords.
- Store password hashes in the database.
- Verify the password on login.

Acceptance criteria:

- `select username, password from users;` does not show plain-text passwords.
- Initial users can log in.
- Newly registered users can log in.

Hint:

For a minimal standard-library implementation, use `hashlib.pbkdf2_hmac()`. In real services, prefer password-storage algorithms or libraries such as Argon2, bcrypt, or scrypt.

## Task G: Level-appropriate Report

Summarize at least one vulnerability.

| Item | What to write |
| --- | --- |
| Root cause | Which implementation was dangerous |
| Observation | What input caused what behavior |
| Fix | What code changed |
| Retest | Whether the same input now fails |
| Remaining risk | What mitigation is still missing |

Experienced participants should also check side effects when multiple mitigations are combined. For example, adding `HttpOnly` makes cookie theft through XSS harder, but it does not remove XSS itself.

