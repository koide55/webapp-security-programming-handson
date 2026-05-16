# トラブルシューティング

演習が止まったときは、症状に近い項目から確認してください。うまくいかない場合は、エラーメッセージをそのまま講師に見せるのが一番早いです。

## 起動できない

### `ModuleNotFoundError: No module named 'bottle'`

原因:

- 仮想環境が有効になっていない
- 依存パッケージが入っていない

確認と修正:

```bash
. .venv/bin/activate
python -m pip install -r requirements.txt
```

### `python: command not found`

環境によっては `python3` を使います。

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

仮想環境を有効にした後は、通常 `python` で実行できます。

### `Address already in use`

すでに同じポートでサーバが起動しています。

対処:

- 以前起動したターミナルで `Ctrl-C` を押す
- 別ポートで起動する

```bash
PORT=18086 python app/main.py --reset-db
```

別ポートで起動した場合、ブラウザでは `http://localhost:18086` を開きます。

### 画面が真っ白、またはブラウザで開けない

確認すること:

- ターミナルに `Listening on http://127.0.0.1:8086/` と表示されているか
- URLが `http://localhost:8086` になっているか
- `https://` ではなく `http://` になっているか
- Webアプリ用と補助サーバ用のポートを取り違えていないか

## ログインできない

初期ユーザを使ってください。

| username | password |
| --- | --- |
| `koide` | `password` |
| `alice` | `alice123` |
| `bob` | `bob123` |

DBを初期化します。

```bash
python app/main.py --reset-db --init-only
```

サーバ起動中の場合は、一度 `Ctrl-C` で止めてから初期化し、再起動してください。

## Cookieが見えない

1. `http://localhost:8086/login` でログインする
2. `http://localhost:8086/cookies` を開く
3. `cookie_id` が表示されるか確認する

表示されない場合:

- ログインに失敗していないか確認する
- `localhost` と `127.0.0.1` を混ぜていないか確認する
- シークレットウィンドウと通常ウィンドウを取り違えていないか確認する
- `/logout` を開いてCookieを消していないか確認する

## 掲示板に入れない

`/bbs` はログインが必要です。

```text
http://localhost:8086/login
```

ログイン後、MyPageからBBSへ移動してください。

## XSS演習で補助サーバに値が出ない

確認すること:

- 補助サーバを別ターミナルで起動しているか
- 補助サーバのURLが `http://localhost:8090` か
- XSSの投稿後、BBSページが再表示されているか
- ブラウザがスクリプトをブロックしていないか

補助サーバを起動します。

```bash
. .venv/bin/activate
python tools/attacker_server.py
```

受信ページを開きます。

```text
http://localhost:8090
```

後片付け:

```bash
sqlite3 app/data.db "delete from comments where comment like '<script>%';"
```

`sqlite3` がない場合は、DBを初期化してください。

```bash
python app/main.py --reset-db --init-only
```

## CSRF演習で投稿されない

確認すること:

- Webアプリでログイン済みか
- 同じブラウザで `http://localhost:8090/csrf` を開いているか
- Webアプリが `http://localhost:8086` で起動しているか
- ブラウザや拡張機能が外部フォーム送信を止めていないか

CSRF演習では、ログイン済みブラウザがCookieを自動送信することを観察します。別ブラウザで補助サーバを開くと、期待どおりに動かないことがあります。

## SQLインジェクション演習で結果が違う

ログイン画面で、実行SQLが表示されているか確認してください。

例:

| username | password |
| --- | --- |
| `koide` | `' or 'a'='a` |
| `koide' --` | `anything` |

コピー時に全角引用符や余計な空白が入ると結果が変わります。`'` は半角のシングルクォートです。

## コマンドインジェクション演習でファイルができない

確認すること:

- `/contact` はログインが必要
- ファイルはリポジトリのルートに作られる
- OSやシェルによって挙動が少し変わる

まずは無害なファイル作成だけを試してください。

```text
"; /bin/echo injected > command_injection_result.txt; #
```

作成確認:

```bash
cat command_injection_result.txt
```

ファイルを消す:

```bash
python tools/clean.py
```

## `sqlite3` コマンドがない

SQLiteの直接確認は任意です。使えない場合は、Webアプリの画面で観察を進めて構いません。

Pythonで簡易確認する場合:

```bash
python -c "import sqlite3; c=sqlite3.connect('app/data.db'); print(c.execute('select userid, username, cookie from users').fetchall())"
```

## Dockerでうまくいかない

ビルドし直します。

```bash
docker compose up --build
```

DBや生成ファイルを消したい場合:

```bash
docker compose down
python tools/clean.py
```

Dockerではコンテナ内から見たパスとホスト側のパスが違うことがあります。演習でファイルを確認する場合は、まずローカルPythonでの実行を推奨します。

## すべて初期状態に戻す

サーバを止めた後、次を実行します。

```bash
python tools/clean.py
. .venv/bin/activate
python app/main.py --reset-db --init-only
```

Windows PowerShellの場合:

```powershell
py tools/clean.py
.\.venv\Scripts\Activate.ps1
python app/main.py --reset-db --init-only
```

その後、Webアプリを再起動します。

```bash
python app/main.py
```
