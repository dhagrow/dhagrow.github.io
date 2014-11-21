<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="A layout example that shows off a blog page with a list of posts.">

  <title>dhagrow</title>

  <link rel="stylesheet" href="/css/pure-min.css">
  <link rel="stylesheet" href="/css/blog.css">
  <link rel="stylesheet" href="/css/source.css">
</head>
<body>

  <div id="layout" class="pure-g">
    <div class="sidebar pure-u-1-5">
      <div class="header">
        <h1 class="brand-title">
          <a href="/">dhagrow</a>
        </h1>
        <h3 class="brand-tagline">prototype</h3>

        <nav class="nav">
          <ul class="nav-list">
            <li class="nav-item">
              <a class="pure-button" href="/gallery">gallery</a>
            </li>
            <li class="nav-item">
              <a class="pure-button" href="/archive">archive</a>
            </li>
          </ul>
        </nav>
      </div>
    </div>

    ${self.body()}

    <div class="footer">omnia mutantur, nos et mutamur in illis</div>
  </div> <!-- layout -->

</body>
</html>
