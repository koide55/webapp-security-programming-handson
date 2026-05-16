# 脆弱性と対策の対応表

| テーマ | 教材内の場所 | 脆弱な実装 | 観察できること | 主な対策 |
| --- | --- | --- | --- | --- |
| セッション管理 | `app/main.py` の `/login`, `/mypage` | DBに `user1` のような推測可能な値を保存する | 盗まれたCookieをコピーするとログイン状態を再現できる | 十分にランダムなセッションID、短い有効期限、再認証、Cookie属性 |
| XSS | `app/views/bbs.tpl` | `{{!comment.comment}}` でエスケープを無効化 | 投稿したJavaScriptが他ユーザのブラウザで実行される | 出力時エスケープ、入力検証、CSP、`HttpOnly` Cookie |
| CSRF | `app/main.py` の `/bbs` | 固定トークンを置くだけで検証しない | 別サイトからログイン中ユーザの権限で投稿できる | セッションごとのCSRFトークン、Origin/Referer検証、SameSite Cookie |
| SQLインジェクション | `app/main.py` の `/login` | SQL文字列にユーザ入力を連結する | パスワードを知らなくてもログインできる | プレースホルダ、ORMの安全なAPI、最小権限 |
| コマンドインジェクション | `app/main.py` の `/contact` | `os.system()` にユーザ入力を連結する | 任意のOSコマンドが実行される | `os.system()` を避ける、`subprocess.run(..., shell=False)`、専用ライブラリ |
| パスワード管理 | `Users.password` | 平文保存 | DB流出時にパスワードが直接漏れる | Argon2/bcrypt/scryptなどのパスワードハッシュ |

## 改修例の方向性

### SQLインジェクション

脆弱な例:

```python
sql = "SELECT * FROM users WHERE username='" + username + "' and password='" + password + "';"
cursor.execute(sql)
```

安全な方向:

```python
cursor.execute(
    "SELECT * FROM users WHERE username=? and password=?;",
    (username, password),
)
```

### XSS

脆弱な例:

```html
{{!comment.comment}}
```

安全な方向:

```html
{{comment.comment}}
```

### コマンドインジェクション

脆弱な例:

```python
os.system('/bin/echo "' + comment + '"')
```

安全な方向:

```python
from pathlib import Path

Path("mail_outbox.txt").write_text(comment, encoding="utf-8")
```

メール送信をしたい場合は、シェルコマンドではなく `smtplib` などの専用ライブラリを使います。
