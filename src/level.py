import random

import pygame

from tile import Tile
from player import Player
from settings import *
from support import import_csv_layout, import_folder

from debug import debug


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        # setup sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.create_map()  # setup sprites
    
    def create_map(self):
        # read and create Tiled map from csv data
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('map/map_Grass.csv'),
            'objects': import_csv_layout('map/map_Objects.csv'),
        }
        graphics= {
            'grass': import_folder('graphics/grass'),
            'objects': import_folder('graphics/objects')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':  # Tiled exports empty tiles as -1
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            # create an invisible wall tile
                            Tile((x,y), [self.obstacle_sprites], 'invisible')
                        elif style == 'grass':
                            # create a grass tile
                            random_image = random.choice(graphics['grass'])
                            Tile((x,y), 
                                 [self.visible_sprites, self.obstacle_sprites], 
                                 'grass', random_image)
                        elif style == 'objects':
                            # create an object tile
                            surf = graphics['objects'][int(col)]
                            Tile((x,y),
                                 [self.visible_sprites, self.obstacle_sprites], 
                                 'object', surf)
        
        # player is a visible sprite, has a reference to obstacle sprites
        self.player = Player((2000, 1430), [self.visible_sprites], 
                             self.obstacle_sprites)

    def run(self):
        # update and draw the game
        self.visible_sprites.update()
        self.visible_sprites.custom_draw(self.player)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2(100, 200)  # camera, offset from the player

        # create the floor
        self.floor_surf = pygame.image.load('graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def custom_draw(self, player):
        # calculate the offset (NOTE: study this code)
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # draw the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)


        for sprite in sorted(self.sprites(), 
                             key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)