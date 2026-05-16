from bottle import get, static_file, template


@get("/static/<filepath:path>")
def static_files(filepath):
    return static_file(filepath, root=str(BASE_DIR / "static"))


@get("/login")
def login_form():
    return template("login", error=None)


def login_error(message):
    return template("login", error=message)
