import pyglet


class Scrollbar:
    def __init__(self, layout, height_offset, scroll_min, color, batch):
        self.layout = layout
        self.height_offset = height_offset
        init_height = (self.layout.content_height - height_offset) / self.layout.height

        self.rect = pyglet.shapes.Rectangle(self.layout.x + self.layout.width - 20, self.layout.y, 20, init_height, color, batch)

    def get_scrollbar_height(self):
        return max(self.layout.height / (self.layout.content_height - self.height_offset), 1)

    def get_scrollbar_pct(self):
        min = self.layout.height - self.layout.content_height
        max = self.height_offset
