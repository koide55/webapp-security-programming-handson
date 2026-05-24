# Source Notes

## Sources

- Gist: <https://gist.github.com/koide55/9ee21387a35eff37bf9c70f9115df128>
- Original slide reference: `slides/webapp-prosecit-20250727.pdf`

## How the Gist Was Turned into Course Material

The original Gist was a minimal single-file web app for demonstrating web app vulnerabilities. This repository keeps that intent while reorganizing the material for hands-on exercises.

- Split `main.py` and BBS HTML into the `app/` directory.
- Updated database connection to `SqliteDatabase` so the app runs with current Python and Peewee.
- Intentionally kept SQL injection, XSS, CSRF, and command injection for observation.
- Replaced crash-prone failure paths with error pages that are easier to observe in class.
- Added a local helper server for XSS, CSRF, and dummy payload distribution.

## Handling

This repository is for understanding vulnerability mechanics and implementing mitigations. Keep all exercise payloads inside the local environment.

