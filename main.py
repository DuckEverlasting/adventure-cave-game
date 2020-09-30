import pygame
from adv import Game

pygame.init()

screen = pygame.display.set_mode((800, 800))

# pygame.display.pygame.display.set_icon(pygame.image.load(""))

running = True
base_font = pygame.font.Font(None, 24)


class TextInput:
    def __init__(self, game, rect=pygame.Rect(200, 600, 400, 24), font=base_font, color=(255, 255, 255)):
        self.text = ""
        self.game = game
        self.rect = rect
        self.font = font
        self.color = color

    def add(self, text):
        text_surface = self.font.render(self.text + text, True, self.color)
        if text_surface.get_width() < self.rect.w - 5:
            self.text += text

    def delete(self):
        self.text = self.text[:-1]

    def submit(self):
        self.game.submit_input(self.text)
        self.text = ""

    def render(self):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        text_surface = self.font.render(self.text, True, self.color)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))


class TextDisplay:
    def __init__(self, rect=pygame.Rect(200, 600, 400, 24), font=base_font, color=(255, 255, 255)):
        self.text = ""
        self.pos_x = 5
        self.pos_y = 5
        self.rect = rect
        self.font = font
        self.color = color

    def print_list(self, items):
        if items is None:
            items = [""]
        for item in items:
            if isinstance(item, str):
                item = {
                    "text": item,
                    "color": (0, 0, 0),
                    "background": None
                }
            string_list = item.text.split("\n")
            text_surface = self.font.render(string_list.pop(0), True, item.color, item.background)
            screen.blit(text_surface, (self.rect.x + self.pos_x, self.rect.y + self.pos_y))
            for other_string in string_list:
                self.pos_y -= self.font.get_height()
                self.pos_x = 5
                text_surface = self.font.render(other_string, True, item.color, item.background)
                screen.blit(text_surface, (self.rect.x + self.pos_x, self.rect.y + self.pos_y))

    def new_line(self):
        self.pos_y -= self.font.get_height()
        self.pos_x = 5

    def clear(self):
        # TODO
        pass

    def get_input(self, prompt):
        # TODO
        pass


text_display = TextDisplay()

game_instance = Game(text_display)
text_input = TextInput(game_instance)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                text_input.submit()
            elif event.key == pygame.K_BACKSPACE:
                text_input.delete()
            else:
                text_input.add(event.unicode)

    screen.fill((0, 0, 0))
    text_input.render()
    pygame.display.update()
