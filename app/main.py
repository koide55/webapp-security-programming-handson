import argparse
import datetime
import html
import os
import sqlite3
from pathlib import Path

from bottle import TEMPLATE_PATH, get, hook, post, redirect, request, response, run, template
from peewee import CharField, ForeignKeyField, Model, PrimaryKeyField, SqliteDatabase


BASE_DIR = Path(__file__).resolve().parent
DBFILE = Path(os.environ.get("DBFILE", BASE_DIR / "data.db"))
OUTBOX_FILE = Path(os.environ.get("OUTBOX_FILE", BASE_DIR / "mail_outbox.txt"))
COOKIE_SECRET = os.environ.get("COOKIE_SECRET", "key")

TEMPLATE_PATH.insert(0, str(BASE_DIR / "views"))

db = SqliteDatabase(str(DBFILE))
last_login_sql = ""


class BaseModel(Model):
    class Meta:
        database = db


class Users(BaseModel):
    userid = PrimaryKeyField()
    username = CharField(null=True, unique=True)
    password = CharField(null=True)
    cookie = CharField(null=True)
    session = CharField(null=True)


class Comments(BaseModel):
    commentid = PrimaryKeyField()
    user = ForeignKeyField(Users, backref="comments")
    comment = CharField(null=False)
    datetime = CharField(null=False)


def initialize_database(reset=False):
    db.connect(reuse_if_open=True)
    if reset:
        db.drop_tables([Comments, Users], safe=True)
        if OUTBOX_FILE.exists():
            OUTBOX_FILE.unlink()
    db.create_tables([Users, Comments])

    if Users.select().count() == 0:
        seed_users = [
            ("koide", "password"),
            ("alice", "alice123"),
            ("bob", "bob123"),
        ]
        for username, password in seed_users:
            Users.create(username=username, password=password)
        koide = Users.get(Users.username == "koide")
        Comments.create(
            user=koide,
            comment="ようこそ。ここは演習用の掲示板です。",
            datetime=datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        )


def render_page(title, body):
    return f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    body {{ font-family: system-ui, sans-serif; line-height: 1.7; margin: 2rem auto; max-width: 760px; }}
    input, textarea, button {{ font: inherit; margin: .25rem 0; }}
    input, textarea {{ box-sizing: border-box; width: 100%; }}
    button {{ cursor: pointer; padding: .35rem .75rem; }}
    nav a {{ margin-right: .5rem; }}
    pre {{ background: #f5f5f5; overflow-x: auto; padding: 1rem; }}
    table {{ border-collapse: collapse; margin: 1rem 0; width: 100%; }}
    th, td {{ border: 1px solid #ddd; padding: .5rem; text-align: left; vertical-align: top; }}
    code {{ overflow-wrap: anywhere; }}
    .error {{ color: #a40000; font-weight: 700; }}
    .ok {{ color: #006c3d; font-weight: 700; }}
    .muted {{ color: #666; }}
  </style>
</head>
<body>
  <h1>{html.escape(title)}</h1>
  {body}
  <hr>
  <nav>
    <a href="/signup">Signup</a>
    <a href="/login">Login</a>
    <a href="/mypage">MyPage</a>
    <a href="/cookies">Cookie</a>
    <a href="/bbs">BBS</a>
    <a href="/contact">Contact</a>
    <a href="/logout">Logout</a>
  </nav>
</body>
</html>"""


def error_page(message, status=400):
    response.status = status
    return render_page("Error", f'<p class="error">{html.escape(message)}</p>')


def current_user():
    cookie_id = request.get_cookie("cookie_id", secret=COOKIE_SECRET)
    if not cookie_id:
        return None
    return Users.get_or_none(Users.cookie == cookie_id)


@hook("before_request")
def before_request():
    response.headers["Access-Control-Allow-Origin"] = "*"


@get("/")
@get("/signup")
def signup_form():
    return render_page(
        "Signup",
        """
        <form action="/register" method="post">
          <label>Username: <input name="username" type="text" autocomplete="username"></label>
          <label>Password: <input name="password" type="password" autocomplete="new-password"></label>
          <button type="submit">Signup</button>
        </form>
        """,
    )


@post("/register")
def register():
    username = request.forms.decode().get("username", "").strip()
    password = request.forms.decode().get("password", "")
    if not username or not password:
        return error_page("username と password を入力してください。")
    if Users.get_or_none(Users.username == username):
        return error_page("その username は登録済みです。")

    Users.create(username=username, password=password)
    return render_page("Registered", '<p class="ok">Registered.</p><p><a href="/login">Go to Login</a></p>')


@get("/hello/<name>")
def hello(name):
    return template("<b>Hello {{name}}</b>", name=name)


@get("/login")
def login_form():
    return render_page(
        "Login",
        """
        <form action="/login" method="post">
          <label>Username: <input name="username" type="text" autocomplete="username"></label>
          <label>Password: <input name="password" type="password" autocomplete="current-password"></label>
          <button type="submit">Login</button>
        </form>
        """,
    )


@post("/login")
def login():
    global last_login_sql
    username = request.forms.decode().get("username", "")
    password = request.forms.decode().get("password", "")

    # Intentionally vulnerable for SQL injection exercises.
    sql = "SELECT * FROM users WHERE username='" + username + "' and password='" + password + "';"
    last_login_sql = sql

    conn = sqlite3.connect(str(DBFILE))
    cursor = conn.cursor()
    try:
        records = cursor.execute(sql)
        record = records.fetchone()
    except sqlite3.Error as exc:
        conn.close()
        return render_page(
            "Login failed",
            f"""
            <p class="error">SQL error: {html.escape(str(exc))}</p>
            <p>Executed SQL:</p>
            <pre>{html.escape(sql)}</pre>
            """,
        )

    if record is None:
        conn.close()
        return render_page(
            "Login failed",
            f"""
            <p class="error">Username or password is wrong.</p>
            <p>Executed SQL:</p>
            <pre>{html.escape(sql)}</pre>
            """,
        )

    cookie_id = "user" + str(record[0])
    response.set_cookie("cookie_id", cookie_id, secret=COOKIE_SECRET)
    cursor.execute("UPDATE users SET cookie=? WHERE userid=?", (cookie_id, record[0]))
    conn.commit()
    conn.close()

    return render_page(
        "Login success",
        f"""
        <p class="ok">Login success. Hello, {html.escape(str(record[1]))}.</p>
        <p>Executed SQL:</p>
        <pre>{html.escape(sql)}</pre>
        <p><a href="/mypage">Go to MyPage</a></p>
        """,
    )


@get("/logout")
def logout():
    response.delete_cookie("cookie_id")
    redirect("/login")


@get("/mypage")
def mypage():
    user = current_user()
    if user is None:
        return error_page("ログインしてください。", status=401)

    return render_page(
        "MyPage",
        f"""
        <p>Hello, {html.escape(user.username)}.</p>
        <ul>
          <li><a href="/bbs">掲示板へ移動</a></li>
          <li><a href="/contact">問い合わせフォームへ移動</a></li>
        </ul>
        """,
    )


@get("/cookies")
def cookies_page():
    raw_cookie_header = request.environ.get("HTTP_COOKIE", "")
    raw_cookie_id = request.cookies.get("cookie_id", "")
    decoded_cookie_id = request.get_cookie("cookie_id", secret=COOKIE_SECRET)
    user = Users.get_or_none(Users.cookie == decoded_cookie_id) if decoded_cookie_id else None

    cookie_rows = []
    for name, value in sorted(request.cookies.items()):
        cookie_rows.append(
            f"""
            <tr>
              <td><code>{html.escape(str(name))}</code></td>
              <td><code>{html.escape(str(value))}</code></td>
            </tr>
            """
        )
    if not cookie_rows:
        cookie_rows.append('<tr><td colspan="2" class="muted">Cookieはまだありません。</td></tr>')

    decoded_value = decoded_cookie_id if decoded_cookie_id else "(なし、または署名検証に失敗)"
    user_label = f"{user.userid}: {user.username}" if user else "(該当ユーザなし)"

    return render_page(
        "Cookie Viewer",
        f"""
        <p>開発者ツールを使わずに、ブラウザが送ってきたCookieを確認するための演習用ページです。</p>

        <h2>Cookie header</h2>
        <pre>{html.escape(raw_cookie_header or "(なし)")}</pre>

        <h2>cookie_id の見え方</h2>
        <table>
          <tr>
            <th>ブラウザに保存されている値</th>
            <td><code>{html.escape(raw_cookie_id or "(なし)")}</code></td>
          </tr>
          <tr>
            <th>署名検証後にアプリが使う値</th>
            <td><code>{html.escape(decoded_value)}</code></td>
          </tr>
          <tr>
            <th>DB上で対応するユーザ</th>
            <td>{html.escape(user_label)}</td>
          </tr>
        </table>

        <h2>すべてのCookie</h2>
        <table>
          <tr><th>名前</th><th>値</th></tr>
          {''.join(cookie_rows)}
        </table>

        <p class="muted">セッションハイジャック演習では、別ブラウザやシークレットウィンドウでログインして、このページの値を比較してください。</p>
        """,
    )


@get("/bbs")
def bbs_form():
    user = current_user()
    if user is None:
        return error_page("ログインしてください。", status=401)

    comments = Comments.select().order_by(Comments.commentid)
    return template("bbs", username=user.username, comments=comments)


@post("/bbs")
def post_bbs():
    user = current_user()
    if user is None:
        return error_page("ログインしてください。", status=401)

    now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    comment = request.forms.decode().get("comment", "")
    Comments.create(user=user, comment=comment, datetime=now)
    redirect("/bbs")


@get("/contact")
def contact_form():
    user = current_user()
    if user is None:
        return error_page("ログインしてください。", status=401)

    return render_page(
        "Contact",
        """
        <form action="/contact" method="post">
          <label>貴方のメールアドレス: <input name="address" type="text"></label>
          <label>連絡事項:
            <textarea name="comment" rows="5" placeholder="連絡事項を書いてください"></textarea>
          </label>
          <button type="submit">送信</button>
        </form>
        """,
    )


@post("/contact")
def contact():
    user = current_user()
    if user is None:
        return error_page("ログインしてください。", status=401)

    address = request.forms.decode().get("address", "")
    comment = request.forms.decode().get("comment", "")

    # Intentionally vulnerable for command injection exercises.
    command = f'/bin/echo "From: {address}\\n{comment}" >> "{OUTBOX_FILE}"'
    exit_code = os.system(command)
    return render_page(
        "Contact sent",
        f"""
        <p class="ok">正常に送信されました。</p>
        <p>Executed shell command:</p>
        <pre>{html.escape(command)}</pre>
        <p>Exit code: {exit_code}</p>
        """,
    )


@get("/debug/last-sql")
def debug_last_sql():
    return render_page("Last Login SQL", f"<pre>{html.escape(last_login_sql)}</pre>")


def main():
    parser = argparse.ArgumentParser(description="Vulnerable Web application for local security training.")
    parser.add_argument("--host", default=os.environ.get("HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8086")))
    parser.add_argument("--reset-db", action="store_true", help="drop and recreate the local SQLite database")
    parser.add_argument("--init-only", action="store_true", help="initialize the database and exit")
    args = parser.parse_args()

    initialize_database(reset=args.reset_db)
    if args.init_only:
        print(f"initialized database: {DBFILE}")
        return
    run(host=args.host, port=args.port, debug=True, reloader=False)


if __name__ == "__main__":
    main()
