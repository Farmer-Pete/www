import random
import string

class ColorGen(object):
    def __init__(self):
        random.seed('LinuxLefty')
        self.colors = list()
        self.base = (155, 155, 155)
        self.light = (255, 255, 255)
        self.dark = (0, 0, 0)
        self.maxAttempts = 10000 # Ten thousand tries

    def mix(self, colorA, colorB):
        return [
            (_color[0] + _color[1]) / 2 for _color in zip(colorA, colorB)
        ]

    def rgb(self, color):
        return 'rgb(%s, %s, %s)' % tuple(color)

    def lighten(self, color):
        return self.mix(color, self.light)

    def darken(self, color):
        return self.mix(color, self.dark)

    def nextColor(self):
        attempt = 0
        while True:

            attempt += 1

            if attempt > self.maxAttempts:
                raise Exception('Exhausted all colors')

            newColor = self.mix(
                self.base,
                [random.randint(0, 255) for _ in range(3)]
            )

            if sum(newColor) > 500:
                # too light
                continue

            if sum(newColor) < 350:
                # Too dark
                continue

            # Now compare this color against previous colors
            for color in self.colors:
                score = sum((
                    abs(_color[0] - _color[1]) for _color in zip(color, newColor)
                ))
                if score < 80:
                    newColor = None
                    break

            if newColor:
                #print 'Attempts = %s' % attempt
                self.colors.append(newColor)
                return newColor

CATEGORIES = [
    'Big_Data', 'Linux' , 'Coding',
    'Security', 'Tools'
]
CATEGORIES.sort()

TEMPLATE = string.Template('''\
#page > header nav ul li.${label} a {
    color: ${color};
    border-color: ${color};
}

@media (max-width:1024px) {
    #page > header nav ul li.${label} a {
        background: ${color};
    }
    #page > header nav ul li.${label}:hover a {
        background: ${color_dark};
        text-shadow: 1px 1px 1px ${color_light};
    }
}

section.boxes article.box.category${label} {
    background: ${color};
    border-color: ${color};
}
section#content.category${label} h2,
section#content.category${label} h3 {
    box-shadow: 0px 0px 15px ${color};
    background: ${color};
}
section#content.category${label} a {
    color: ${color_dark};
}
section#content.category${label} div.summary img,
section#content.category${label} img,
section#content.category${label} svg {
    border-color: ${color};
}
section#content.category${label} span.icon span.icon-tag {
    background-color: ${color};
}
section#content.category${label} span.icon span.icon-tag:before {
    border-color: ${color} transparent transparent ${color} !important;
}
section#content.category${label} span.icon span.icon-tag:after {
    border-color: ${color} ${color} transparent transparent !important;
}
section#content.category${label} code {
    background: ${color_light};
    color: inherit;
}
''')

def gen(target):
    colorGen = ColorGen()

    with open(target, 'w') as f:
        for label in CATEGORIES:
            color = colorGen.nextColor()

            f.write(TEMPLATE.substitute(
                label=label,
                label_lower=label.lower(),
                color=colorGen.rgb(color),
                color_light=colorGen.rgb(colorGen.lighten(color)),
                color_dark=colorGen.rgb(colorGen.darken(color))
            ))
