#! /usr/bin/env python

"""
jen.py

A static website generator.
"""

import io
import os
import collections
from datetime import datetime

import hoep
import profig
from mako import template
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

ROOT_DIR = os.path.dirname(__file__)
POSTS_DIR = 'content/posts'
TEMPLATE_DIR = 'templates'

class Renderer(hoep.Hoep):
    def block_code(self, text, language):
        lexer = get_lexer_by_name(language or 'text', stripall=True)
        formatter = HtmlFormatter(linenos=True, cssclass='source')
        return highlight(text, lexer, formatter)

def render(s):
    return Renderer(hoep.EXT_FENCED_CODE).render(s)

class Meta(collections.namedtuple('Meta', 'title tags date')):
    @classmethod
    def from_file(cls, file):
        cfg = profig.Config(file)
        
        cfg.format.delimeter = b': '
        cfg.coercer.register(datetime,
            lambda x: x.isoformat(b' '),
            lambda x: datetime.strptime(x, b'%Y-%m-%d %H:%M'))
        
        sec = cfg.section('default')
        sec.init('tags', [])
        sec.init('date', datetime.now())
        
        cfg.read()
        return cls(**sec)

class Post(object):
    def __init__(self, meta, content):
        self.meta = meta
        self.content = content
    
    @classmethod
    def from_file(self, file):
        meta_buf = io.BytesIO()
        content_buf = io.BytesIO()
        state = None
        
        for line in file:
            sline = line.strip()
            
            if state == 'content':
                content_buf.write(line)
            
            elif state == 'metadata':
                if sline.endswith('---'):
                    state = 'content'
                    continue
                meta_buf.write(line)
            
            elif sline.startswith('---'):
                state = 'metadata'
            
            else:
                content_buf.write(line)
        
        meta = Meta.from_file(meta_buf)
        content = render(content_buf.getvalue().decode('utf8'))
        return Post(meta, content)

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
