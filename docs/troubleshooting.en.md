# Troubleshooting

When an exercise stops, start with the item closest to your symptom. If you still cannot proceed, show the full error message to the instructor.

## The App Does Not Start

### `ModuleNotFoundError: No module named 'bottle'`

Possible causes:

- The virtual environment is not active.
- Dependencies are not installed.

Check and fix:

```bash
. .venv/bin/activate
python -m pip install -r requirements.txt
```

### `python: command not found`

Some environments use `python3`.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

After activating the virtual environment, `python` usually works.

### `Address already in use`

A server is already using the same port.

Options:

- Press `Ctrl-C` in the terminal that started the old server.
- Start on another port.

```bash
PORT=18086 python app/main.py --reset-db
```

If you use a different port, open `http://localhost:18086`.

### The page is blank or the browser cannot open it

Check:

- Does the terminal show `Listening on http://127.0.0.1:8086/`?
- Is the URL `http://localhost:8086`?
- Are you using `http://`, not `https://`?
- Did you mix up the web app port and the helper server port?

## Login Fails

Use the initial users.

| username | password |
| --- | --- |
| `koide` | `password` |
| `alice` | `alice123` |
| `bob` | `bob123` |

Reset the database:

```bash
python app/main.py --reset-db --init-only
```

If the server is running, stop it with `Ctrl-C`, initialize the DB, and restart it.

## Cookies Are Not Visible

1. Log in at `http://localhost:8086/login`.
2. Open `http://localhost:8086/cookies`.
3. Check whether `cookie_id` is displayed.

If not:

- Confirm login succeeded.
- Do not mix `localhost` and `127.0.0.1`.
- Confirm which window is normal and which is incognito.
- Confirm you did not open `/logout` and delete the cookie.

## Cannot Open BBS

`/bbs` requires login.

```text
http://localhost:8086/login
```

After login, move from MyPage to BBS.

## XSS Value Does Not Reach the Helper Server

Check:

- Is the helper server running in another terminal?
- Is the helper URL `http://localhost:8090`?
- Was the BBS page redisplayed after posting the XSS payload?
- Did the browser block the script?

Start the helper server:

```bash
. .venv/bin/activate
python tools/attacker_server.py
```

Open the receiver page:

```text
http://localhost:8090
```

Cleanup:

```bash
sqlite3 app/data.db "delete from comments where comment like '<script>%';"
```

If `sqlite3` is unavailable, reset the DB:

```bash
python app/main.py --reset-db --init-only
```

## CSRF Exercise Does Not Post

Check:

- Are you logged in to the web app?
- Did you open `http://localhost:8090/csrf` in the same browser?
- Is the web app running at `http://localhost:8086`?
- Is a browser extension blocking cross-site form submission?

The CSRF exercise observes that a logged-in browser automatically sends cookies. If you open the helper page in a different browser, the expected behavior may not occur.

## SQL Injection Result Is Different

On the login page, confirm that the executed SQL is displayed.

Examples:

| username | password |
| --- | --- |
| `koide` | `' or 'a'='a` |
| `koide' --` | `anything` |

Full-width quotes or extra spaces can change the result. The quote character must be the ASCII single quote `'`.

## Command Injection File Is Not Created

Check:

- `/contact` requires login.
- The file is created in the repository root.
- Shell behavior may differ slightly by OS and shell.

First try the harmless file creation example.

```text
"; /bin/echo injected > command_injection_result.txt; #
```

Check:

```bash
cat command_injection_result.txt
```

Clean:

```bash
python tools/clean.py
```

## `sqlite3` Is Not Installed

Direct SQLite inspection is optional. If you cannot use `sqlite3`, continue observing through the web app.

Quick check using Python:

```bash
python -c "import sqlite3; c=sqlite3.connect('app/data.db'); print(c.execute('select userid, username, cookie from users').fetchall())"
```

## Docker Problems

Rebuild:

```bash
docker compose up --build
```

To remove generated files:

```bash
docker compose down
python tools/clean.py
```

Paths inside the container and paths on the host can differ. For file-observation exercises, local Python execution is recommended first.

## Reset Everything

Stop the server, then run:

```bash
python tools/clean.py
. .venv/bin/activate
python app/main.py --reset-db --init-only
```

Windows PowerShell:

```powershell
py tools/clean.py
.\.venv\Scripts\Activate.ps1
python app/main.py --reset-db --init-only
```

Then restart the web app:

```bash
python app/main.py
```

