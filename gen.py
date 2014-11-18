import os
import shutil

import hoep
from mako import template

SITE_DIR = 'site'
POSTS_DIR = 'content/posts'
TEMPLATE_DIR = 'templates'

def ensure_dir(path):
    try:
        os.makedirs(path)
    except OSError:
        pass

def gather_posts():
    for fname in os.listdir(POSTS_DIR):
        fname = os.path.join(POSTS_DIR, fname)
        with open(fname) as file:
            yield file.read()

def main():
    ensure_dir(SITE_DIR)
    
    # gather posts
    posts = gather_posts()
    
    # render templates
    for fname in os.listdir(TEMPLATE_DIR):
        print 'rendering:', fname
        
        fname = os.path.join(TEMPLATE_DIR, fname)
        tmpl = template.Template(filename=fname)
        
        rendered = tmpl.render(posts=posts)
        
        out_fname = os.path.join(SITE_DIR, os.path.basename(fname))
        with open(out_fname, 'w+') as file:
            file.write(rendered)
    
    # copy static files
    shutil.copytree('css', os.path.join(SITE_DIR, 'css'))

if __name__ == '__main__':
    main()
