# Prerequisites

This page is a starting point before the exercises. You do not need to memorize everything. When you get stuck, return here and check the terms and flow.

## What We Use

| Area | Used for | Minimum understanding |
| --- | --- | --- |
| Code editor | Editing files and using a terminal | Open a folder, edit files, and open a terminal |
| Terminal | Starting apps, checking the DB, starting the helper server | Run commands one line at a time |
| Python | Running the Bottle app | Start the server with `python app/main.py` |
| HTTP | Browser and web server communication | There are requests and responses |
| HTML | Display and XSS | Browsers interpret HTML tags |
| Cookie | Login state and sessions | The browser stores values and sends them on later requests |
| SQL | Storing users and comments | SQL queries data in a database |
| Shell | Command injection | Characters such as `;` and `"` have syntax meaning |

## Recommended Editor

For beginners, this material standardizes on **Visual Studio Code**. It is free and works on Windows, macOS, and Linux. It also keeps Python support, an integrated terminal, and Git integration in one place, which makes classroom explanations easier to follow.

The editor used here is **Visual Studio Code**, not **Visual Studio**.

If you already have an editor you like, you may keep using it. The instructor's screen examples will assume VS Code.

### Install and Prepare VS Code

1. Download VS Code from the official site: <https://code.visualstudio.com/Download>
2. Run the installer with the default settings.
   - Windows: choose `User Installer x64`.
   - macOS: choose `Universal` or the build that matches your Mac.
   - Linux: choose `.deb` for Ubuntu/Debian or `.rpm` for Fedora-based systems.
3. Start VS Code.
4. Open the Extensions view, search for `Python`, and install the Python extension from Microsoft.
5. Use `File` > `Open Folder...` and open the `webapp-security-programming-handson` repository folder.
6. Use `Terminal` > `New Terminal`.
7. After setup, if VS Code asks for a Python interpreter, select the Python inside `.venv`.

Run the course commands in the VS Code terminal.

## Terminal Basics

Move to the repository root:

```bash
cd webapp-security-programming-handson
```

Activate the virtual environment:

```bash
. .venv/bin/activate
```

Start the web app:

```bash
python app/main.py --reset-db
```

Start the helper server in another terminal:

```bash
python tools/attacker_server.py
```

To stop a running server, press `Ctrl-C` in the terminal that started it.

## HTTP Basics

When you open a URL, the browser sends an HTTP request to the web server. The server returns an HTTP response.

Common HTTP methods in this material:

| Method | Examples | Role |
| --- | --- | --- |
| GET | `/login`, `/bbs`, `/cookies` | Retrieve a page or information |
| POST | `/login`, `/register`, `/bbs`, `/contact` | Submit form data |

In the exercises, watch where a value submitted through a form is interpreted as code.

## Cookies and Sessions

HTTP does not remember previous requests by itself. Web apps use cookies to keep login state.

In this material, the app issues `cookie_id` after login.

How to check it:

1. Log in as `koide` / `password`.
2. Open `http://localhost:8086/cookies`.
3. Compare the value stored in the browser with the value the app uses after verification.

Important points:

- Cookies are stored in the browser.
- The browser sends cookies with requests to the same site.
- If a cookie is stolen, login state may be reproduced.
- Attributes such as `HttpOnly`, `SameSite`, and `Secure` change what the cookie is protected from.

## HTML Escaping

In HTML, a string such as `<script>` is interpreted as a tag.

User input:

```html
<script>alert(1)</script>
```

To display it safely, the app must render it as text, not as a tag.

```html
&lt;script&gt;alert(1)&lt;/script&gt;
```

The BBS template intentionally uses `{{!comment.comment}}` to disable escaping for the XSS exercise.

## SQL Basics

Example SQL for finding a user in SQLite:

```sql
select * from users where username='koide';
```

The dangerous pattern is concatenating user input directly into an SQL string.

```python
sql = "SELECT * FROM users WHERE username='" + username + "';"
```

The safer direction is to separate the SQL structure from input values.

```python
cursor.execute("SELECT * FROM users WHERE username=?;", (username,))
```

## Shell Basics

In a shell, these characters have syntax meaning:

| Character | Example meaning |
| --- | --- |
| `"` | String delimiter |
| `;` | Command separator |
| `#` | Start of a comment |
| `|` | Pipe output to the next command |

If user input is concatenated into a shell command, it may be interpreted as a different command.

This material observes the behavior safely by creating only local files.

## Pre-exercise Checklist

Before starting, confirm that:

- `python --version` or `python3 --version` works.
- `python app/main.py --reset-db` starts the web app.
- `http://localhost:8086` opens in your browser.
- You can log in with `koide` / `password`.
- `http://localhost:8086/cookies` opens the cookie page.
- `python tools/attacker_server.py` starts in another terminal.
- `http://localhost:8090` opens in your browser.

