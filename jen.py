#! /usr/bin/env python

"""
jen.py

A static website generator.
"""

import os

import hoep
from mako import template

ROOT_DIR = os.path.dirname(__file__)
POSTS_DIR = 'content/posts'
TEMPLATE_DIR = 'templates'

def gather_posts():
    for fname in os.listdir(POSTS_DIR):
        fname = os.path.join(POSTS_DIR, fname)
        with open(fname) as file:
            yield file.read()

def main():
    # gather posts
    posts = gather_posts()
    
    # render templates
    for fname in os.listdir(TEMPLATE_DIR):
        print 'rendering:', fname
        
        fname = os.path.join(TEMPLATE_DIR, fname)
        tmpl = template.Template(filename=fname)
        
        rendered = tmpl.render(posts=posts)
        
        out_fname = os.path.join(ROOT_DIR, os.path.basename(fname))
        with open(out_fname, 'w+') as file:
            file.write(rendered)

if __name__ == '__main__':
    main()
