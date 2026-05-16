# Web Application Security Programming Hands-on

Webアプリケーションの代表的な脆弱性を、ローカル環境で観察するための教材リポジトリです。添付スライド `webapp-prosecit-20250727.pdf` と、Gistの演習用Bottleアプリをもとに、現行のPythonで動かせる形に整理しています。

この教材は防御学習用です。アプリには、SQLインジェクション、XSS、CSRF、コマンドインジェクションを意図的に残しています。公開サーバや共有ネットワーク上では起動しないでください。

## 構成

```text
.
├── app/
│   ├── main.py              # 演習用の脆弱Webアプリ
│   └── views/bbs.tpl        # 掲示板テンプレート
├── tools/
│   ├── attacker_server.py   # XSS/CSRF/ダミーペイロード用の補助サーバ
│   └── clean.py             # 演習生成ファイルの削除
├── docs/
│   ├── setup.md             # 環境構築
│   ├── prerequisites.md     # 事前知識
│   ├── exercises.md         # 演習手順
│   ├── troubleshooting.md   # よくある詰まりどころ
│   ├── advanced-tasks.md    # 経験者向け発展課題
│   ├── instructor-notes.md  # 講師向けメモ
│   ├── instructor-hints.md  # 講師用ヒント
│   ├── solutions.md         # 解答例
│   └── security-notes.md    # 脆弱性と対策の対応表
├── examples/
│   └── pico-css/            # Pico.cssでUIを整えるサンプル
├── slides/
│   └── README.md
├── requirements.txt
├── Dockerfile
└── compose.yaml
```

## Quick Start

```bash
git clone https://github.com/koide55/webapp-security-programming-handson.git
cd webapp-security-programming-handson
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python app/main.py --reset-db
```

ブラウザで `http://localhost:8086` を開きます。初期ユーザは次の通りです。

| username | password |
| --- | --- |
| `koide` | `password` |
| `alice` | `alice123` |
| `bob` | `bob123` |

XSS、CSRF、コマンドインジェクションの一部演習では、別ターミナルで補助サーバも起動します。

```bash
. .venv/bin/activate
python tools/attacker_server.py
```

補助サーバは `http://localhost:8090` で起動します。

## 教材の進め方

1. [事前知識](docs/prerequisites.md)
2. [環境構築](docs/setup.md)
3. [演習手順](docs/exercises.md)
4. [トラブルシューティング](docs/troubleshooting.md)
5. [脆弱性と対策の対応表](docs/security-notes.md)
6. [経験者向け発展課題](docs/advanced-tasks.md)
7. [講師向けメモ](docs/instructor-notes.md)
8. [講師用ヒント](docs/instructor-hints.md)
9. [解答例](docs/solutions.md)
10. [参照元と教材化メモ](docs/source-notes.md)

元Gist: <https://gist.github.com/koide55/9ee21387a35eff37bf9c70f9115df128>
