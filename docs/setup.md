# 環境構築

この教材はローカルPCだけで完結します。外部に公開しない前提で、意図的に脆弱なWebアプリを起動します。

## 必要なもの

- Python 3.11以降
- pip
- Webブラウザ
- 任意: Docker / Docker Compose
- 任意: SQLiteを直接見るための `sqlite3` コマンド

## Pythonで起動する

リポジトリのルートで実行します。

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python app/main.py --reset-db
```

起動後、ブラウザで次を開きます。

```text
http://localhost:8086
```

初期ユーザ:

| username | password |
| --- | --- |
| `koide` | `password` |
| `alice` | `alice123` |
| `bob` | `bob123` |

データベースを初期状態に戻す場合:

```bash
. .venv/bin/activate
python app/main.py --reset-db --init-only
```

## 補助サーバを起動する

XSS、CSRF、コマンドインジェクションの演習では、別ターミナルで補助サーバを起動します。

```bash
. .venv/bin/activate
python tools/attacker_server.py
```

起動後、次を開けます。

```text
http://localhost:8090
```

補助サーバの役割:

- `/` はXSSで送られてきたCookie文字列を記録します。
- `/csrf` はCSRF実験用のページです。
- `/badscript` はコマンドインジェクション演習用の無害なダミーペイロードです。

## Dockerで起動する

ローカルPython環境を汚したくない場合はDockerを使えます。

```bash
docker compose up --build
```

Webアプリ:

```text
http://localhost:8086
```

補助サーバ:

```text
http://localhost:8090
```

## よくあるトラブル

### `ModuleNotFoundError: No module named 'bottle'`

仮想環境が有効になっているか確認し、依存パッケージを入れ直してください。

```bash
. .venv/bin/activate
python -m pip install -r requirements.txt
```

### ポートが使われている

別のポートを指定できます。

```bash
PORT=18086 python app/main.py
PORT=18090 python tools/attacker_server.py
```

### 演習結果を消したい

次のファイルは演習中に生成されます。削除して構いません。

- `app/data.db`
- `app/mail_outbox.txt`
- `stolen_cookies.log`
- `command_injection_result.txt`
- `downloaded_badscript.py`
- `badscript_ran.txt`

まとめて消す場合:

```bash
make clean
```
