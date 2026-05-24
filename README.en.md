# Web Application Security Programming Hands-on

This repository is a training kit for observing common web application vulnerabilities in a local environment. It reorganizes the original slide material and the Bottle sample app into a Git-based hands-on project that runs on current Python.

Japanese entry point: [README.md](README.md).

This material is for defensive learning. The app intentionally contains SQL injection, XSS, CSRF, command injection, weak session handling, and plain-text password storage. Do not run it on a public server or on a shared network.

## Contents

```text
.
|-- app/
|   |-- main.py              # Vulnerable training web app
|   `-- views/bbs.tpl        # BBS template
|-- tools/
|   |-- attacker_server.py   # Local helper for XSS, CSRF, and dummy payloads
|   `-- clean.py             # Removes files generated during exercises
|-- docs/
|   |-- setup.en.md             # Environment setup
|   |-- prerequisites.en.md     # Prerequisites
|   |-- exercises.en.md         # Student exercises
|   |-- troubleshooting.en.md   # Common problems
|   |-- advanced-tasks.en.md    # Advanced tasks
|   |-- instructor-notes.en.md  # Instructor notes
|   |-- instructor-hints.en.md  # Instructor facilitation hints
|   |-- solutions.en.md         # Example answers
|   `-- security-notes.en.md    # Vulnerability-to-mitigation map
|-- examples/
|   `-- pico-css/            # Pico.css sample
|-- slides/
|   |-- webapp-security-programming-updated-content.en.md
|   `-- webapp-security-programming-handson-2026-en.pptx
|-- requirements.txt
|-- Dockerfile
`-- compose.yaml
```

## Quick Start

```bash
git clone https://github.com/koide55/webapp-security-programming-handson.git
cd webapp-security-programming-handson
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python app/main.py --reset-db
```

Open the app in your browser:

```text
http://localhost:8086
```

Initial users:

| username | password |
| --- | --- |
| `koide` | `password` |
| `alice` | `alice123` |
| `bob` | `bob123` |

Some XSS, CSRF, and command injection exercises also use the local helper server. Start it in a second terminal:

```bash
. .venv/bin/activate
python tools/attacker_server.py
```

The helper server runs at:

```text
http://localhost:8090
```

## Suggested Order

1. [Prerequisites](docs/prerequisites.en.md)
2. [Environment Setup](docs/setup.en.md)
3. [Exercises](docs/exercises.en.md)
4. [Troubleshooting](docs/troubleshooting.en.md)
5. [Security Notes](docs/security-notes.en.md)
6. [Advanced Tasks](docs/advanced-tasks.en.md)
7. [Instructor Notes](docs/instructor-notes.en.md)
8. [Instructor Hints](docs/instructor-hints.en.md)
9. [Solutions](docs/solutions.en.md)
10. [Source Notes](docs/source-notes.en.md)

Original Gist: <https://gist.github.com/koide55/9ee21387a35eff37bf9c70f9115df128>
