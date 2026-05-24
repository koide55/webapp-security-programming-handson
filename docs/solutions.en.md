# Solutions

This file is for instructors or for checking advanced tasks. If students receive it at the beginning, the observation phase may become too short. Facilitation prompts and hints are separated into `docs/instructor-hints.en.md`.

## Exercise 0: Startup Check

Expected state:

- `http://localhost:8086` opens.
- `koide` / `password` logs in.
- A BBS post can be submitted.
- `app/data.db` is created.

Command:

```bash
. .venv/bin/activate
python app/main.py --reset-db
```

## Exercise 1: Bottle Routing

Checkpoints:

- `@get("/hello/<name>")` connects a URL pattern to a function.
- The `<name>` value becomes the function argument `name`.
- `template()` generates and returns an HTML string.

URLs:

```text
http://localhost:8086/hello/security
http://localhost:8086/hello/alice
```

## Exercise 2: Peewee and SQLite

Expected observations:

- The `users` and `comments` tables exist.
- `users.password` stores plain-text passwords.
- `comments.user_id` refers to the author.

SQL:

```sql
.tables
.schema users
.schema comments
select userid, username, password, cookie from users;
select commentid, user_id, comment, datetime from comments;
```

## Exercise 3: Session Hijacking

Expected observations:

- `/cookies` compares the browser-stored value and the value after signature verification.
- `/cookies` can replace the browser-stored cookie value.
- `/cookies` can create a signed cookie from an internal value such as `user1`.
- The raw signed cookie value is a long string.
- Internally, the app restores a value such as `user1`.
- Copying a cookie can reproduce login state.

Notes:

- Because `secret=COOKIE_SECRET` is used, manually typing `user1` as the browser-stored value does not work.
- Signing detects tampering. It does not prevent cookie leakage.
- The change form on `/cookies` is an exercise helper and should not exist in a real service.

## Exercise 4: XSS

Root cause:

```html
{{!comment.comment}}
```

Fix example:

```html
{{comment.comment}}
```

Retest:

- Post `<script>alert(1)</script>`.
- Confirm the script does not execute and is displayed as text.

## Exercise 5: CSRF

Fix example:

```python
import secrets

def ensure_csrf_token(user):
    if not user.session:
        user.session = secrets.token_urlsafe(32)
        user.save()
    return user.session
```

GET `/bbs`:

```python
token = ensure_csrf_token(user)
return template("bbs", username=user.username, comments=comments, token=token)
```

POST `/bbs`:

```python
token = request.forms.decode().get("token", "")
if not user.session or token != user.session:
    return error_page("CSRF token is invalid.", status=403)
```

Template:

```html
<input type="hidden" name="token" value="{{token}}">
```

Retest:

- Posting from the BBS page succeeds.
- Posting from `http://localhost:8090/csrf` returns 403.

## Exercise 6: SQL Injection

Root cause:

```python
sql = "SELECT * FROM users WHERE username='" + username + "' and password='" + password + "';"
records = cursor.execute(sql)
```

Fix example:

```python
records = cursor.execute(
    "SELECT * FROM users WHERE username=? and password=?;",
    (username, password),
)
record = records.fetchone()
```

Retest:

| username | password | Expected result |
| --- | --- | --- |
| `koide` | `password` | Login succeeds |
| `koide` | `' or 'a'='a` | Login fails |
| `koide' --` | `anything` | Login fails |

## Exercise 7: Command Injection

Root cause:

```python
command = f'/bin/echo "From: {address}\n{comment}" >> "{OUTBOX_FILE}"'
exit_code = os.system(command)
```

Fix example:

```python
with OUTBOX_FILE.open("a", encoding="utf-8") as outbox:
    outbox.write(f"From: {address}\n")
    outbox.write(comment)
    outbox.write("\n---\n")
```

Retest:

- Normal contact submission succeeds.
- The command injection string does not create `command_injection_result.txt`.
- `app/mail_outbox.txt` stores the input as text.

## Exercise 8: Pico.css UI Cleanup

Expected state:

- Shared navigation is moved to `base.tpl`.
- `login.tpl` has a clearer form structure.
- Pico.css styles `label`, `input`, `button`, and `nav` with little custom CSS.

Sample files:

- `examples/pico-css/views/base.tpl`
- `examples/pico-css/views/login.tpl`
- `examples/pico-css/static/app.css`
- `examples/pico-css/main_snippet.py`

## Exercise 9: Fix the Vulnerabilities

Acceptance criteria:

| Task | Retest |
| --- | --- |
| SQLi fix | `' or 'a'='a` cannot log in |
| XSS fix | `<script>` is displayed as text |
| Cookie attributes | The student can explain `HttpOnly` and `SameSite` |
| CSRF fix | Posting from helper `/csrf` fails |
| Command injection fix | `command_injection_result.txt` is not created |
| Password hashing | Plain-text passwords are not visible in the DB |

Presentation template:

```text
Vulnerability:
Root cause:
Input tested:
Observed behavior:
Fix:
Retest result:
Remaining risk:
```

