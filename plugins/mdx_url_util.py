import re
import string
import markdown
import pelicanconf

class UrlUtil_external(markdown.postprocessors.Postprocessor):
    """ Adds rel="nofollow" and target="_blank" to links """

    RE = re.compile(r'''<a (?P<old>[^>]*http.?://)''')

    def run(self, text):
        return self.RE.sub('<a target="_blank" rel="nofollow" \g<old>', text)

class UrlUtil_shortlinks(markdown.postprocessors.Postprocessor):
    """ Replaces short links with longer ones """

    CONFIG = (
            ('wp', "en.wikipedia.org/wiki/\g<href>"),
            ('arch', "wiki.archlinux.org/index.php/\g<href>"),
        )


    RE = [
            [
                re.compile(r'''
                            (?P<markup><\s*[^\>]*
                                (?:href|src)\s*=\s*
                            )
                            "%s:
                            (?P<href>[^"]*)"
                        ''' % find, re.X),
                '\g<markup>"http://%s"' % replace
            ] for find, replace in CONFIG
    ]

    def run(self, text):

        for find, replace in self.RE:
            text = find.sub(replace, text)

        return text

class UrlUtil_autotags(markdown.postprocessors.Postprocessor):
    """ Automatically discover tags based on links. Also links in categories """

    RE_tag = re.compile(r'''<a\ href="tag:([^"]+)">([^<]+)</a>''')
    RE_cat = re.compile(r'''<a\ href="cat:([^"]+)">([^<]+)</a>''')

    SUB_tag = '''<a href="%(url)s" title="See posts tagged with '%(tag_str)s'">%(label)s</a><span class="icon icon-small"><span class="icon-tag"></span></span>'''
    SUB_cat = '''<a href="%(url)s" title="See posts which exist the '%(category_str)s' category">%(label)s</a><span class="icon icon-small"><span class="icon-tag"></span></span>'''

    def run(self, text):

        tags = set((
            _.strip() for _ in
            self.markdown.Meta.get('tags', [''])[0].split(',')
        ))

        def capture_tags(match):
            tag, label = match.groups()
            tags.add(tag.lower())
            return self.SUB_tag % {
                'label': label,
                'tag': tag,
                'tag_str': tag.replace('_', ' '),
                'url': '../' + pelicanconf.TAG_URL.replace('{slug}', tag.lower())
            }

        def handle_categories(match):
            category, label = match.groups()
            category = category.lower()

            return self.SUB_cat % {
                'label': label,
                'category': category,
                'category_str': category.replace('_', ' '),
                'url': '../' + pelicanconf.CATEGORY_URL.replace('{name}', category.lower())
            }

        result = self.RE_tag.sub(capture_tags, text)
        result = self.RE_cat.sub(handle_categories, result)

        if tags:
            self.markdown.Meta['tags'] = [', '.join(tags)] 

        return result

class UrlUtils(markdown.Extension):
    """ Add nofollow for links to Markdown. """

    def extendMarkdown(self, md, md_globals):
        md.postprocessors.add('urlutil_external', UrlUtil_external(md), '_end')
        md.postprocessors.add('urlutil_shortlinks', UrlUtil_shortlinks(md), '<urlutil_external') # Runs before external runs
        md.postprocessors.add('urlutil_autotags', UrlUtil_autotags(md), '<urlutil_shortlinks') # Runs before shortlinks runs

def makeExtension(configs=None):
    return UrlUtils(configs=configs)
