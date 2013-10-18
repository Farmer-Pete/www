#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

_ROOT = '/home/tirian/personal/blog/linuxlefty'

DEBUG = True

AUTHOR = u'Peter Naudus'
SITENAME = u'LinuxLefty'

USE_FOLDER_AS_CATEGORY = True
DEFAULT_CATEGORY = 'misc'
DEFAULT_DATE = 'fs'
FILENAME_METADATA = r'(?P<date>\d{4}-\d{2}-\d{2})_(?P<slug>.*)'

PATH = _ROOT + '/content'
OUTPUT_PATH = _ROOT + '/output'

SITEURL = 'file://' + OUTPUT_PATH

THEME = _ROOT + '/theme'

TIMEZONE = 'America/New_York'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

DEFAULT_PAGINATION = 10

MD_EXTENSIONS = [ 'codehilite', 'extra', 'url_util' ]
PLUGINS = [ 'thumber' ]
PLUGIN_PATH = _ROOT + '/plugins'
STATIC_PATHS = [".thumbs"]

TYPOGRIFY = True

ARTICLE_URL = '{category}/{slug}.html'
ARTICLE_SAVE_AS = '{category}/{slug}.html'

CATEGORY_URL = '{slug}/index.html'
CATEGORY_SAVE_AS = '{slug}/index.html'

TAG_URL = 'tag/{slug}.html'
TAG_SAVE_AS = 'tag/{slug}.html'

THUMBS = _ROOT + '/content/.thumbs'
THUMB_SIZE = (210, 210)

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# Load plugin path for markdown plugins
import sys
sys.path.append(PLUGIN_PATH)

# Generate custom CSS
import os
_CSS = THEME + '/static/css'
if not os.path.exists(_CSS + '/categories.css') or os.stat(_CSS + '/categories.py').st_mtime > os.stat(_CSS + '/categories.css').st_mtime:
    print "Generating CSS ..."
    sys.path.append(_CSS)
    import categories
    categories.gen(_CSS + '/categories.css')
    del sys.path[-1]

