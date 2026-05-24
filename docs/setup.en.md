# Environment Setup

This training environment is designed to run entirely on your local machine. The web app is intentionally vulnerable, so keep it local and do not expose it to the internet.

## Requirements

- Python 3.11 or later
- pip
- A web browser
- Optional: Docker and Docker Compose
- Optional: the `sqlite3` command for inspecting the database directly

## Clone the Repository

From any working directory, clone the training repository from GitHub.

```bash
git clone https://github.com/koide55/webapp-security-programming-handson.git
cd webapp-security-programming-handson
```

Run the following commands from the repository root.

## Run with Python

macOS or Linux:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python app/main.py --reset-db
```

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python app/main.py --reset-db
```

After the server starts, open:

```text
http://localhost:8086
```

Initial users:

| username | password |
| --- | --- |
| `koide` | `password` |
| `alice` | `alice123` |
| `bob` | `bob123` |

To reset the database without starting the server:

```bash
. .venv/bin/activate
python app/main.py --reset-db --init-only
```

## Start the Helper Server

The XSS, CSRF, and command injection exercises use a helper server. Start it in a separate terminal.

```bash
. .venv/bin/activate
python tools/attacker_server.py
```

Open:

```text
http://localhost:8090
```

The helper server provides:

- `/` - receives and displays cookie strings sent during the XSS exercise.
- `/csrf` - serves the CSRF demo page.
- `/badscript` - serves a harmless dummy payload for the command injection exercise.

## Run with Docker

If you do not want to modify your local Python environment, use Docker.

```bash
docker compose up --build
```

Web app:

```text
http://localhost:8086
```

Helper server:

```text
http://localhost:8090
```

## Common Setup Problems

### `ModuleNotFoundError: No module named 'bottle'`

Activate the virtual environment and reinstall dependencies.

```bash
. .venv/bin/activate
python -m pip install -r requirements.txt
```

### The port is already in use

Use another port.

```bash
PORT=18086 python app/main.py
PORT=18090 python tools/attacker_server.py
```

### Clean generated exercise files

The exercises may generate these files:

- `app/data.db`
- `app/mail_outbox.txt`
- `stolen_cookies.log`
- `command_injection_result.txt`
- `downloaded_badscript.py`
- `badscript_ran.txt`

Clean them with:

```bash
python tools/clean.py
```

On Windows PowerShell, use:

```powershell
py tools/clean.py
```

On macOS or Linux, `make clean` performs the same cleanup when `make` is installed.

```bash
make clean
```

Most Windows environments do not include `make` by default, so use `python tools/clean.py` or `py tools/clean.py`.

