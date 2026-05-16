# Pico.css Sample

演習8「Pico.cssでシンプルに整える」で使うサンプルです。既存のBottleアプリに対して、HTML文字列を少しずつテンプレートへ移し、Pico.cssを1枚読み込むだけでフォーム、ボタン、表、ナビゲーションを整える方針です。

## 追加する構成

```text
app/
├── static/
│   └── app.css
└── views/
    ├── base.tpl
    └── login.tpl
```

このサンプルディレクトリには、上記ファイルと `main_snippet.py` を置いています。

## 1. 静的ファイル配信を追加する

`app/main.py` に次のルートを追加します。

```python
@get("/static/<filepath:path>")
def static_files(filepath):
    return static_file(filepath, root=str(BASE_DIR / "static"))
```

`bottle` から `static_file` をimportしていない場合は、import行に追加します。

```python
from bottle import TEMPLATE_PATH, get, hook, post, redirect, request, response, run, static_file, template
```

## 2. ログイン画面をテンプレート化する

既存の `login_form()` を次のように置き換えます。

```python
@get("/login")
def login_form():
    return template("login", error=None)
```

ログイン失敗時も同じテンプレートを使う場合:

```python
return template("login", error="Username or password is wrong.")
```

## 3. Pico.cssを読み込む

`views/base.tpl` の `<head>` でPico.cssを読み込みます。

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">
<link rel="stylesheet" href="/static/app.css">
```

Pico.cssはセマンティックHTMLをそのまま整えるため、多数のクラスを覚える必要がありません。

## 4. 観察ポイント

- `label`、`input`、`button`、`table`、`nav` が少ないCSSで整う。
- 共通ナビゲーションを `base.tpl` に集約できる。
- セキュリティ上の実装と、見た目の改善を分離できる。
- UI改善のついでに、XSS対策としてテンプレートのエスケープ有無も確認できる。
