# Instructor Notes

## Mapping to Slides

| Slide range | Repository material |
| --- | --- |
| p.3-p.4 Web app experiment environment | `docs/setup.en.md` |
| p.5-p.10 Bottle / Peewee / SQLite | Exercises 1 and 2 |
| p.11-p.28 Session management and session hijacking | Exercise 3 |
| p.29-p.40 XSS | Exercise 4 |
| p.41-p.45 CSRF | Exercise 5 |
| p.46-p.49 SQL injection | Exercise 6 |
| p.50-p.59 Command injection | Exercise 7 |
| p.60-p.66 Clean up the UI with Pico.css | Exercise 8 |
| Advanced and wrap-up | Exercise 9 |

## Suggested Timing

| Time | Content |
| --- | --- |
| 10 min | Environment setup and startup check |
| 15 min | Bottle, Peewee, and SQLite |
| 20 min | Session hijacking |
| 25 min | XSS |
| 20 min | CSRF |
| 20 min | SQL injection |
| 25 min | Command injection |
| 20 min | UI cleanup with Pico.css |
| 30 min | Fix tasks and presentations |

## Points to Emphasize

- Do not focus on memorizing attack strings. Focus on where data becomes code.
- Cookie, HTML, SQL, and shell all have different contexts.
- "Do not trust input" is not enough. Handle data correctly for the output context.
- Even in local exercises, ask students to explain the role of the helper server and dummy payloads.

## Handling Different Skill Levels

- For beginners, point them first to `docs/prerequisites.en.md` and `docs/troubleshooting.en.md`.
- In the standard flow, make the observation points in `docs/exercises.en.md` mandatory.
- For fast finishers, assign one or more tasks from `docs/advanced-tasks.en.md`.
- Use `docs/instructor-hints.en.md` for prompts and `docs/solutions.en.md` for answer checking.

## Safety Notes

- The normal Python app listens on `127.0.0.1`. Docker uses `0.0.0.0` for port publishing, so be careful on shared networks.
- Keep command injection examples limited to harmless file creation.
- At the beginning, explicitly confirm that students must not test these payloads against external sites, school systems, or third-party services.

## Main Improvements from the Original Gist

- Uses `SqliteDatabase` so the Peewee models run on current Python.
- Fixes the `datetime.now()` reference issue.
- Avoids crashes on unauthenticated access or failed login.
- Exposes observation points for SQLi, XSS, CSRF, and command injection in the UI and documentation.
- Adds a helper server for XSS, CSRF, and dummy payload distribution.
- Supports both Python virtual environments and Docker.

