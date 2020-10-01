import pyglet
from adv import Game

window = pyglet.window.Window()

running = True


class TextInput:
    def __init__(self, game, x, y, width):
        self.game = game
        self.document = pyglet.text.decode_text('')
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

    def submit(self):
        self.game.submit_input(self.text)
        self.document.text = ""
        self.caret.move_to_point(self.layout.x, self.layout.y)


class TextDisplay:
    def __init__(self):
        self.text = pyglet.text.decode_attributed('')
        self.layout = None
        self.font = None
        self.color = None

    def print_list(self, text=""):
        # TODO
        pass

    def clear(self):
        # TODO
        pass

    def get_input(self, prompt):
        # TODO
        pass


text_display = TextDisplay()
game_instance = Game(text_display)
text_input = TextInput(game_instance)
game_instance.game_boot()

pyglet.app.run()
