#! /usr/bin/env python

"""
jen.py

A static website generator.
"""

import io
import os
import collections

import hoep
import profig
from mako import template

ROOT_DIR = os.path.dirname(__file__)
POSTS_DIR = 'content/posts'
TEMPLATE_DIR = 'templates'

class JenFormat(profig.IniFormat):
    delimeter = b': '

Meta = collections.namedtuple('Meta', 'title tags date')

class Post(object):
    def __init__(self, meta, content):
        self.meta = Meta(**meta)
        self.content = content
        print self.meta
        print self.content
    
    @classmethod
    def from_file(self, file):
        content = io.BytesIO()
        metadata = io.BytesIO()
        state = None
        
        for line in file:
            sline = line.strip()
            
            if state == 'content':
                content.write(line)
            
            elif state == 'metadata':
                if sline.endswith('---'):
                    state = 'content'
                    continue
                metadata.write(line)
            
            elif sline.startswith('---'):
                state = 'metadata'
            
            else:
                content.write(line)
        
        meta = profig.Config(metadata, format=JenFormat)
        meta.init('default.tags', [])
        meta.read()
        
        return Post(meta.section('default'), content.getvalue())

def gather_posts():
    for fname in os.listdir(POSTS_DIR):
        fname = os.path.join(POSTS_DIR, fname)
        with open(fname) as file:
            yield Post.from_file(file)

def main():
    # gather posts
    posts = list(gather_posts())
    
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
