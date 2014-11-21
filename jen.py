#! /usr/bin/env python

"""
jen.py

A static website generator.
"""

import io
import os
import itertools
import collections
from datetime import datetime

import hoep
import profig
from mako import template
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

ROOT_DIR = os.path.dirname(__file__)
POSTS_DIR = os.path.join(ROOT_DIR, 'content/posts')
POSTS_OUTPUT_DIR = os.path.join(ROOT_DIR, 'posts')
TEMPLATE_DIR = os.path.join(ROOT_DIR, 'templates')

def ensure_dir(path):
    try:
        os.makedirs(path)
    except OSError:
        pass

class Renderer(hoep.Hoep):
    def __init__(self):
        ext = hoep.EXT_FENCED_CODE | hoep.EXT_HIGHLIGHT
        super(Renderer, self).__init__(ext)
    
    def block_code(self, text, language):
        lexer = get_lexer_by_name(language or 'text', stripall=True)
        formatter = HtmlFormatter(linenos=True, cssclass='source')
        return highlight(text, lexer, formatter)

class Meta(collections.namedtuple('Meta', 'title category tags date sticky')):
    @classmethod
    def from_file(cls, file):
        cfg = profig.Config(file)
        
        cfg.format.delimeter = b': '
        cfg.coercer.register(datetime,
            lambda x: x.isoformat(b' '),
            lambda x: datetime.strptime(x, b'%Y-%m-%d %H:%M'))
        
        sec = cfg.section('default')
        sec.init('title', '')
        sec.init('category', '')
        sec.init('tags', [])
        sec.init('date', datetime.now())
        sec.init('sticky', False)
        
        cfg.read()
        return cls(**sec)
    
    @property
    def date_text(self):
        return self.date.strftime('%Y | %b %d | %H:%M')

class Post(object):
    def __init__(self, name, meta, content):
        self.name = name
        self.meta = meta
        self.content = content
    
    @classmethod
    def from_file(self, name, file):
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
        content = Renderer().render(content_buf.getvalue().decode('utf8'))
        return Post(name, meta, content)

def gather_posts():
    for fname in os.listdir(POSTS_DIR):
        fname = os.path.join(POSTS_DIR, fname)
        name = os.path.splitext(os.path.basename(fname))[0]
        with open(fname) as file:
            yield Post.from_file(name, file)

def main():
    # gather posts
    sort_key = lambda p: (
        p.meta.sticky, p.meta.date, p.meta.category, p.meta.date)
    group_key = lambda p: p.meta.category
    
    posts = sorted(gather_posts(), key=sort_key, reverse=True)
    categories = itertools.groupby(posts, group_key)
    
    # render index
    print 'rendering: index'
    
    fname = os.path.join(TEMPLATE_DIR, 'index.tpl')
    tmpl = template.Template(filename=fname)
    
    rendered = tmpl.render(categories=categories)
    
    out_fname = os.path.join(ROOT_DIR, os.path.basename(fname))
    with open(out_fname, 'w+') as file:
        file.write(rendered)
    
    # render posts
    for post in posts:
        print 'rendering:', post.name
        
        fname = os.path.join(TEMPLATE_DIR, 'post.tpl')
        tmpl = template.Template(filename=fname)
        
        categories = [(post.meta.category, [post])]
        rendered = tmpl.render(categories=categories)
        
        ensure_dir(POSTS_OUTPUT_DIR)
        out_fname = os.path.join(POSTS_OUTPUT_DIR,
            os.extsep.join([post.name, 'html']))
        with open(out_fname, 'w+') as file:
            file.write(rendered)

if __name__ == '__main__':
    main()
