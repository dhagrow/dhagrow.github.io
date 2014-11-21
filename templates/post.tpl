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
        <h1 class="brand-title">dhagrow</h1>
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

    <div id="content" class="content pure-u-4-5">
      <div id="posts">
        <div class="posts">
      
      %for category, posts in categories:
          <h1 class="content-subhead">${category}</h1>
        %for post in posts:
          <section class="post">
            <header class="post-header">
            %if post.meta.title:
              <h2 class="post-title">${post.meta.title}</h2>
            %endif
              <div class="post-date">${post.meta.date_text}</div>
              <p class="post-meta">
              %for tag in post.meta.tags:
                <a class="post-category post-category-${tag}" href="#">${tag}</a>
              %endfor
              </p>
            </header>

            <div class="post-description">
              <p>
                ${post.content}
              </p>
            </div>
          </section>
        %endfor
      %endfor
        
        </div>

        <div class="footer">omnia mutantur, nos et mutamur in illis</div>
        
      </div> <!-- posts -->
    </div> <!-- content -->
  </div> <!-- layout -->

</body>
</html>
