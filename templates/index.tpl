<%inherit file="base.tpl"/>

<div id="content" class="content pure-u-4-5">
  <div id="posts" class="posts">
    
  %for category, posts in categories:
    <h1 class="content-subhead">${category}</h1>
    
  %for post in posts:
    <section class="post">
      <header class="post-header">
    
      %if post.meta.title:
        <h2 class="post-title">
          <a href="/posts/${post.name}.html">${post.meta.title}</a>
        </h2>
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
    
  </div> <!-- posts -->
</div> <!-- content -->
