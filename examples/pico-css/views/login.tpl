% rebase("base.tpl", title="Login")

<article>
  <header>
    <h1>Login</h1>
    <p>演習用Webアプリにログインします。</p>
  </header>

  % if error:
    <p role="alert" class="notice-error">{{error}}</p>
  % end

  <section>
    <h2>初期ユーザ</h2>
    <table>
      <thead>
        <tr><th>Username</th><th>Password</th></tr>
      </thead>
      <tbody>
        <tr><td><code>koide</code></td><td><code>password</code></td></tr>
        <tr><td><code>alice</code></td><td><code>alice123</code></td></tr>
        <tr><td><code>bob</code></td><td><code>bob123</code></td></tr>
      </tbody>
    </table>
  </section>

  <form action="/login" method="post">
    <label>
      Username
      <input name="username" type="text" autocomplete="username" required>
    </label>

    <label>
      Password
      <input name="password" type="password" autocomplete="current-password" required>
    </label>

    <div class="actions">
      <button type="submit">Login</button>
      <a href="/signup" role="button" class="secondary">Signup</a>
    </div>
  </form>
</article>
