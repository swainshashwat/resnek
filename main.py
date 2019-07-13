import pygame
from pygame.locals import *

class Player:
    x = 10
    y = 10
    speed = 1

    def moveRight(self):
        self.x = self.x + self.speed
    
    def moveLeft(self):
        self.x = self.x - self.speed
    
    def moveUp(self):
        self.y = self.y + self.speed
    
    def moveDown(self):
        self.y = self.y - self.speed


class App:
    windowWidth = 800
    windowHeight = 600
    player = 0

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self.player = Player()
    
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(
                            (self.windowWidth, self.windowHeight),
                            pygame.HWSURFACE)
        pygame.display.set_caption('Reinforcement Snek Game')