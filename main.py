import pyglet
from adv import Game


class TextInput:
    def __init__(self, game, x, y, width, fg, bg):
        self.game = game
        self.document = pyglet.text.document.UnformattedDocument()
        self.document.set_style(
            0,
            len(self.document.text),
            {"color": (0, 0, 0, 255)}
        )
        font = self.document.get_font()
        height = font.ascent - font.descent
        self.background = pyglet.shapes.Rectangle(x, y - 5, width, height + 10, color=(255, 255, 255), batch=bg)

        self.layout = pyglet.text.layout.IncrementalTextLayout(
            self.document,
            width - 10,
            height,
            multiline=False,
            batch=fg
        )
        self.caret = pyglet.text.caret.Caret(self.layout)

        self.layout.x = x + 5
        self.layout.y = y

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.RETURN:
            self.submit()
            return True

    def submit(self):
        self.game.submit_command(self.document.text)
        self.document.delete_text(0, len(self.document.text))
        self.caret.move_to_point(self.layout.x, self.layout.y)


class TextDisplay:
    def __init__(self, x, y, width, height, fg, bg):
        self.document = pyglet.text.document.FormattedDocument(" ")
        self.layout = pyglet.text.layout.ScrollableTextLayout(
            self.document,
            width - 10,
            height - 10,
            multiline=True,
            batch=fg
        )
        self.background = pyglet.shapes.Rectangle(x, y, width, height, color=(255, 255, 255), batch=bg)
        self.layout.x = x + 5
        self.layout.y = y + 5

    def print_text(self, text=""):
        formatted = pyglet.text.decode_attributed(text)
        self.document.insert_text(len(self.document.text), formatted.text)
        self.layout.view_y = self.layout.height - self.layout.content_height


    def clear(self):
        self.document.text = ""


window = pyglet.window.Window(width=800, height=800)
fg_batch = pyglet.graphics.Batch()
bg_batch = pyglet.graphics.Batch()

left = window.width * .125 // 1
bottom = window.height * .300 // 1
bottom_2 = window.height * .125 // 1
w = window.width * .75 // 1
h = window.height * .5 // 1

text_display = TextDisplay(left, bottom, w, h, fg_batch, bg_batch)
game_instance = Game(text_display)
text_input = TextInput(game_instance, left, bottom_2, w, fg_batch, bg_batch)
window.push_handlers(text_input.caret)
window.push_handlers(text_input.on_key_press)


@window.event
def on_draw():
    window.clear()
    bg_batch.draw()
    fg_batch.draw()


@window.event
def on_text(text):
    if text == "\r":
        return True


pyglet.app.run()
