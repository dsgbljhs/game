import pygame
import os
import pyganim

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
ICON_DIR = os.path.dirname(__file__)  # Полный путь к каталогу с файлами

ANIMATION_PRINCESS = [
    ('%s/blocks/princess_l.png' % ICON_DIR),
    ('%s/blocks/princess_r.png' % ICON_DIR)]


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(pygame.Color(PLATFORM_COLOR))
        self.image = pygame.image.load("%s/blocks/platform.png" % ICON_DIR)
        self.rect = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class BlockDie(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.image.load("%s/blocks/dieBlock.png" % ICON_DIR)


class BlockDi(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.image.load("%s/blocks/fire1.png" % ICON_DIR)


class Princess(Platform):
    image =  pygame.image.load("%s/blocks/princess_r.png" % ICON_DIR)
    mask = pygame.mask.from_surface(image)
    rect = image.get_rect()

    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.image.load("%s/blocks/princess_r.png" % ICON_DIR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.image.fill(pygame.Color(PLATFORM_COLOR))
        self.boltAnim.blit(self.image, (0, 0))

