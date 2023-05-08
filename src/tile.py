import pygame

from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, 
                 surface = pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.image = surface
        if sprite_type == 'object':
            # move larger images up 1 tile
            self.rect = self.image.get_rect(topleft=(pos[0],pos[1]-TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.sprite_type = sprite_type
        