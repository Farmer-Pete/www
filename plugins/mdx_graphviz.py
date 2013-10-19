import markdown, re, markdown.preprocessors, subprocess

class GraphvizExtension(markdown.Extension):
    def reset(self):
        pass

    def extendMarkdown(self, md, md_globals):
        "Add GraphvizExtension to the Markdown instance."
        md.registerExtension(self)
        md.preprocessors.add('graphviz', GraphvizPreprocessor(md), '_begin')

class GraphvizPreprocessor(markdown.preprocessors.Preprocessor):
    "Find all graphviz blocks, generate images and inject image link to generated images."

    FILTERS = ["dot", "neato", "twopi", "circo", "fdp"]
    START_TAG_RE = re.compile(r'''^\s*<graphviz\s*([^>]*)>''')
    END_TAG_RE = re.compile(r'''^\s*</graphviz>''')
    SVG_OPEN_TAG_RE = re.compile(r'''^\s*<svg width="\d+pt" height="\d+pt"(.*)''')

    def run(self, lines):
        result = []
        block = []
        blockOptions = {}
        insideBlock = False
        for line in lines:
            startTag = self.START_TAG_RE.search(line)

            if startTag:
                insideBlock = True
                blockOptions = self.getGraphConfig(startTag.groups()[0])
                continue

            endTag = self.END_TAG_RE.search(line)

            if endTag:
                result.extend([
                    '<div class="svgWrapper">',
                    ' '.join(self.getGraphSVG(block, blockOptions)),
                    '</div>'
                ])
                insideBlock = False
                del block[:]
            elif insideBlock:
                block.append(line)
            else:
                result.append(line)

        return result

    def getGraphConfig(self, configStr):
        # Convert configStr to a dict
        configDict = dict((
            (_.strip('"\'') for _ in pair.split('='))
            for pair in configStr.split(' ') if pair
        ))

        if 'filter' not in configDict:
            raise ValueError('graphviz object given, but no filter specified')
        if configDict['filter'] not in self.FILTERS:
            raise ValueError('Unknown filter specified: "%s"' % configDict['filter'])

        return configDict

    def getGraphSVG(self, lines, configDict):
        command = [configDict['filter'], '-Tsvg']

        # Add additional options
        command += [
                    '-%s=%s' % (key, value)
                    for key, value in configDict.items()
                    if key != 'filter'
                ]

        p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)

        p.stdin.write('\n'.join(lines))
        p.stdin.close()
        p.wait()

        svgTagFound = False

        # First, discard any lines that precede the <svg> tag (doctype, etc)
        # Then, yeild all following lines
        for line in p.stdout:
            if svgTagFound:
                yield line.strip()
            else:
                openTag = self.SVG_OPEN_TAG_RE.match(line)
                if openTag:
                    svgTagFound = True

                    # Replace the default width/height with 100%
                    yield '<svg width="100%" height="100%"' + openTag.groups()[-1]

def makeExtension(configs=None) :
    return GraphvizExtension(configs=configs)
