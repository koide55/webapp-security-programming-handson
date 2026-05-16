<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light dark">
  <title>{{title or "WebApp Security"}}</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">
  <link rel="stylesheet" href="/static/app.css">
</head>
<body>
  <header class="container">
    <nav>
      <ul>
        <li><strong>WebApp Security</strong></li>
      </ul>
      <ul>
        <li><a href="/signup">Signup</a></li>
        <li><a href="/login">Login</a></li>
        <li><a href="/mypage">MyPage</a></li>
        <li><a href="/cookies">Cookie</a></li>
        <li><a href="/bbs">BBS</a></li>
        <li><a href="/contact">Contact</a></li>
        <li><a href="/logout">Logout</a></li>
      </ul>
    </nav>
  </header>

  <main class="container">
    {{!base}}
  </main>
</body>
</html>
