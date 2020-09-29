import pygame
from adv import Game

pygame.init()

screen = pygame.display.set_mode((800,800))


# pygame.display.pygame.display.set_icon(pygame.image.load(""))

running = True
base_font = pygame.font.Font(None,24)

class Parser:
    def parse(self, text):
        return text

class TextInput:
    def __init__(self, game, rect=pygame.Rect(200, 600, 400, 24), font=base_font, color=(255,255,255)):
        self.text = ""
        self.game = game
        self.rect = rect
        self.font = font
        self.color = color
        self.parser = Parser()

    def add(self, text):
        text_surface = self.font.render(self.text + text, True, self.color)
        if (text_surface.get_width() < self.rect.w - 5):
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

class Screen:
    def __init__(self):
        # TODO
        pass

    def print(self):
        # TODO
        pass

    def clear(self):
        # TODO
        pass

    def getInput(self):
        # TODO
        pass

game = Game(Screen())
text_input = TextInput(game)

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
                
    screen.fill((0,0,0))
    text_input.render()
    pygame.display.update()