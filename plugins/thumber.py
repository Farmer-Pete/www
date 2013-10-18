import os
import urllib2
import tempfile

from PIL import Image
from pelican import signals
from pelicanconf import THUMBS, THUMB_SIZE

def register():
    signals.article_generator_context.connect(thumbs)
    #signals.article_generator_preread.connect(tmp)

def tmp(generator):
    import pdb; pdb.set_trace()

def thumbs(generator, metadata):

    if not metadata.get('thumb'):
        return

    if not metadata.get('slug'):
        raise Exception('No slug: %s' % metadata)

    target = os.path.join(THUMBS, metadata['slug'] + '.png')

    if not os.path.exists(target):
        print 'Downloading thumbnail for %s/%s ... %s' % (metadata['category'].name, metadata['slug'], metadata['thumb'])

        request = urllib2.Request(metadata['thumb'])
        request.add_header('User-Agent', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Win64; x64; Trident/6.0)')

        response = urllib2.urlopen(request)

        with tempfile.NamedTemporaryFile() as f:
            f.write(response.read())
            f.seek(0)

            image = Image.open(f.name)
            image.thumbnail(THUMB_SIZE, Image.ANTIALIAS)

        image.save(target, "PNG")
