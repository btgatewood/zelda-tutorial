import pygame

from settings import *
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('data/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-26)  # the rect follows the hitbox

        self.import_graphics()
        self.status = 'down'

        self.direction = pygame.math.Vector2()
        self.speed = 5

        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = 0

        self.obstacle_sprites = obstacle_sprites
    
    def import_graphics(self):
        self.animations = {'up':[], 'down':[], 'left':[], 'right':[],
                           'up_idle':[], 'down_idle':[], 'left_idle':[], 'right_idle':[],
                           'up_attack':[], 'down_attack':[], 'left_attack':[], 'right_attack':[]}
        path = 'graphics/player/'

        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)

    
    def input(self):
        keys = pygame.key.get_pressed()

        # movement
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        # attack
        if keys[pygame.K_SPACE] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            print('attack')
        
        # magic
        if keys[pygame.K_LCTRL] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            print('magic')
    
    def get_status(self):
        pass

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        # self.rect.center += self.direction * speed
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center
    
    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right
                    elif self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left    

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom
                    elif self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
    
    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        # simple attack timer
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                print('attacking = False')
                self.attacking = False

    
    def update(self):
        self.input()
        self.cooldowns()
        self.move(self.speed)