# Security Notes

| Topic | Location | Vulnerable implementation | What to observe | Main mitigations |
| --- | --- | --- | --- | --- |
| Session management | `/login`, `/mypage` in `app/main.py` | Stores predictable values such as `user1` in the DB | Copying a stolen cookie can reproduce login state | Random session IDs, short expiration, reauthentication, cookie attributes |
| XSS | `app/views/bbs.tpl` | Disables escaping with `{{!comment.comment}}` | Posted JavaScript runs in another user's browser | Output escaping, input validation, CSP, `HttpOnly` cookies |
| CSRF | `/bbs` in `app/main.py` | Includes a fixed token but does not verify it | Another site can post with the logged-in user's authority | Per-session CSRF tokens, Origin/Referer checks, SameSite cookies |
| SQL injection | `/login` in `app/main.py` | Concatenates user input into SQL | Login may succeed without the password | Placeholders, safe ORM APIs, least privilege |
| Command injection | `/contact` in `app/main.py` | Concatenates user input into `os.system()` | Arbitrary OS commands may run | Avoid `os.system()`, use `subprocess.run(..., shell=False)`, use dedicated libraries |
| Password management | `Users.password` | Plain-text storage | If the DB leaks, passwords are directly exposed | Password hashing with Argon2, bcrypt, scrypt, or similar |

## Fix Directions

### SQL Injection

Vulnerable example:

```python
sql = "SELECT * FROM users WHERE username='" + username + "' and password='" + password + "';"
cursor.execute(sql)
```

Safer direction:

```python
cursor.execute(
    "SELECT * FROM users WHERE username=? and password=?;",
    (username, password),
)
```

### XSS

Vulnerable example:

```html
{{!comment.comment}}
```

Safer direction:

```html
{{comment.comment}}
```

### Command Injection

Vulnerable example:

```python
os.system('/bin/echo "' + comment + '"')
```

Safer direction:

```python
from pathlib import Path

Path("mail_outbox.txt").write_text(comment, encoding="utf-8")
```

If you need real email delivery, use a dedicated library such as `smtplib` instead of shell commands.

### Password Hashing

Do not store passwords in plain text. If the database leaks, stored values should not reveal the original passwords directly.

Do not use a simple SHA-256 hash for passwords. Use a salted, intentionally expensive password hashing method. In production, prefer Argon2, bcrypt, scrypt, or a library that wraps them. For a minimal exercise that uses only the Python standard library, `hashlib.pbkdf2_hmac()` is acceptable.

Store the algorithm name, iteration count, salt, and digest together in one string so verification and future migration are easier.

```python
import base64
import hashlib
import hmac
import secrets

ITERATIONS = 200_000


def b64encode(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        ITERATIONS,
    )
    return f"pbkdf2_sha256${ITERATIONS}${b64encode(salt)}${b64encode(digest)}"
```

At login time, fetch the user by username, hash the submitted password with the same parameters, and compare it to the stored value. Use `hmac.compare_digest()` rather than `==` to reduce timing side-channel risk.

```python
def verify_password(password: str, stored: str) -> bool:
    try:
        method, iterations, salt_text, digest_text = stored.split("$")
    except ValueError:
        return False

    if method != "pbkdf2_sha256":
        return False

    salt = base64.b64decode(salt_text)
    expected = base64.b64decode(digest_text)
    actual = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        int(iterations),
    )
    return hmac.compare_digest(actual, expected)
```

In the exercise app, use `hash_password()` when creating initial users and when registering new users. During login, do not include the password directly in the SQL condition. Fetch the user by username and then verify the password with `verify_password()`.

