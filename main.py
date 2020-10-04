import pyglet
from game import Game
from history import History

"""
TODO:
- set pauses where appropriate
- get better graphics
- get text display to anchor to bottom correctly
- get scroll working
- get previous command cache working (borrow from Gazorkazork?)
- test game for bugs
- add content to game???
- add sound???????
"""


class TextInput:
    def __init__(self, game, x, y, width, fg, bg):
        self.game = game
        self.history = History()
        self.document = pyglet.text.document.UnformattedDocument()
        self.document.set_style(
            0,
            len(self.document.text),
            {"color": (255, 255, 255, 255)}
        )
        self.font = self.document.get_font()
        height = self.font.ascent - self.font.descent
        self.background = pyglet.shapes.Rectangle(x, y - 20, width, height + 40, color=(0, 0, 0), batch=bg)

        self.layout = pyglet.text.layout.IncrementalTextLayout(
            self.document,
            width - 40,
            height,
            multiline=False,
            batch=fg
        )
        self.caret = pyglet.text.caret.Caret(self.layout, color=(255, 255, 255))

        self.layout.x = x + 20
        self.layout.y = y

    def submit(self):
        self.game.submit_command(self.document.text)
        self.history.push(self.document.text)
        self.document.delete_text(0, len(self.document.text))
        self.caret.position = 0

    def prev(self):
        prev_text = self.history.get_prev()
        if prev_text is not None:
            self.document.text = prev_text
            self.caret.position = len(self.document.text)

    def next(self):
        next_text = self.history.get_next()
        self.document.text = next_text
        self.caret.position = len(self.document.text)


class TextDisplay:
    def __init__(self, x, y, width, height, fg, bg):
        self.init_text = "{font_name 'Courier New'}{font_size 12}{color (255, 255, 255, 255)}" + "\n\n"
        self.current_text = self.init_text
        document = pyglet.text.decode_attributed(self.init_text)
        self.layout = pyglet.text.layout.ScrollableTextLayout(
            document,
            width - 40,
            height - 40,
            multiline=True,
            batch=fg
        )
        self.background = pyglet.shapes.Rectangle(x, y, width, height, color=(0, 0, 0), batch=bg)
        self.y_max = y
        self.layout.x = x + 20
        self.layout.y = min(self.layout.content_height, self.y_max) + 20
        self.layout.view_y = self.layout.height - self.layout.content_height
        self.clock = pyglet.clock.Clock()

    def print_text(self, text=""):
        self.current_text += (text + "\n\n")
        self.update_document()

    def clear(self):
        self.current_text = self.init_text
        self.update_document()

    def update_document(self):
        self.layout.document = pyglet.text.decode_attributed(self.current_text)
        self.layout.y = min(self.layout.content_height, self.y_max) + 20
        self.layout.view_y = self.layout.height - self.layout.content_height

    def wait(self, pause=.75):
        elapsed = 0
        while elapsed <= pause:
            elapsed += self.clock.tick()


# noinspection PyMethodMayBeStatic
class AppController:
    def __init__(self):
        self.window = pyglet.window.Window(width=1200, height=800)
        pyglet.gl.glClearColor(0.15, 0.15, 0.15, 1)
        self.fg_batch = pyglet.graphics.Batch()
        self.bg_batch = pyglet.graphics.Batch()

        left = self.window.width * .125 // 1
        bottom = self.window.height * .300 // 1
        bottom_2 = self.window.height * .125 // 1
        w = self.window.width * .75 // 1
        h = self.window.height * .5 // 1

        self.display = TextDisplay(left, bottom, w, h, self.fg_batch, self.bg_batch)
        self.game_instance = Game(self)
        self.input = TextInput(self.game_instance, left, bottom_2, w, self.fg_batch, self.bg_batch)
        self.window.push_handlers(self.input.caret)
        self.window.push_handlers(self.on_draw, self.on_key_press, self.on_text)
        self.submit_on_any_key = True

        self.game_instance.game_boot()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.RETURN or self.submit_on_any_key is True:
            self.input.submit()
            return True
        elif symbol == pyglet.window.key.UP:
            self.input.prev()
            return True
        elif symbol == pyglet.window.key.DOWN:
            self.input.next()
            return True

    def on_draw(self):
        self.window.clear()
        self.bg_batch.draw()
        self.fg_batch.draw()

    def on_text(self, text):
        if text == "\r" or self.submit_on_any_key:
            self.submit_on_any_key = False
            return True


app_controller = AppController()
pyglet.app.run()
