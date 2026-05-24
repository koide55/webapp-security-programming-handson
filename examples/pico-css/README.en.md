# Pico.css Sample

This sample is used in Exercise 8, "Clean up the UI with Pico.css." The idea is to move the existing Bottle app's HTML strings into templates gradually, then load one Pico.css stylesheet to improve forms, buttons, tables, and navigation.

## Added Structure

```text
app/
|-- static/
|   `-- app.css
`-- views/
    |-- base.tpl
    `-- login.tpl
```

This sample directory contains those files plus `main_snippet.py`.

## 1. Add Static File Serving

Add this route to `app/main.py`.

```python
@get("/static/<filepath:path>")
def static_files(filepath):
    return static_file(filepath, root=str(BASE_DIR / "static"))
```

If `static_file` is not imported from `bottle`, add it to the import line.

```python
from bottle import TEMPLATE_PATH, get, hook, post, redirect, request, response, run, static_file, template
```

## 2. Move the Login Page into a Template

Replace the existing `login_form()` with:

```python
@get("/login")
def login_form():
    return template("login", error=None)
```

If login failure uses the same template:

```python
return template("login", error="Username or password is wrong.")
```

## 3. Load Pico.css

Load Pico.css from the `<head>` in `views/base.tpl`.

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">
<link rel="stylesheet" href="/static/app.css">
```

Pico.css styles semantic HTML, so students do not need to memorize many utility classes.

## 4. Observation Points

- `label`, `input`, `button`, `table`, and `nav` become readable with little custom CSS.
- Shared navigation can be centralized in `base.tpl`.
- Security implementation and visual cleanup can be discussed separately.
- While improving UI, students can also review where templates escape or do not escape output for XSS.
