import pyglet


class TextInput(object):
    def __init__(self, x, y, width):
        self.document = pyglet.text.decode_text("")
        self.document.set_style(
            0,
            len(self.document.text),
            {"color": (0, 0, 0, 255)}
        )
        font = self.document.get_font()
        height = font.ascent - font.descent

        self.layout = pyglet.text.layout.IncrementalTextLayout(
            self.document,
            width,
            height,
            multiline=False
        )
        self.caret = pyglet.text.caret.Caret(self.layout)

        self.layout.x = x
        self.layout.y = y

        # Rectangular outline
        # RECT SHAPE GOES HERE

    def hit_test(self, x, y):
        return (0 < x - self.layout.x < self.layout.width and
                0 < y - self.layout.y < self.layout.height)
