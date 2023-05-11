import pygame

from settings import *
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, 
                 create_attack, destroy_attack):
        super().__init__(groups)
        self.image = pygame.image.load('data/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-26)  # the rect follows the hitbox

        self.obstacle_sprites = obstacle_sprites

        self.import_graphics()  # load data
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15

        self.direction = pygame.math.Vector2()
        self.speed = 5

        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack

        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.weapon_changing = False
        self.weapon_switch_cooldown = 200
        self.weapon_switch_time = None
        
    
    def import_graphics(self):
        path = 'data/player/'
        self.animations = {'up':[], 'down':[], 'left':[], 'right':[],  # walk
                           'up_idle':[], 'down_idle':[], 
                           'left_idle':[], 'right_idle':[],
                           'up_attack':[], 'down_attack':[], 
                           'left_attack':[], 'right_attack':[]}
        
        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        if self.attacking:  # ignore input during attack state
            return

        keys = pygame.key.get_pressed()

        # movement
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0

        # attack
        if keys[pygame.K_SPACE]:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.create_attack()
        
        # magic
        if keys[pygame.K_LCTRL]:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            print('magic')
        
        # change weapon
        if keys[pygame.K_q] and not self.weapon_changing:
            self.weapon_changing = True
            self.weapon_switch_time = pygame.time.get_ticks()
            self.weapon_index += 1
            if self.weapon_index == len(weapon_data):
                self.weapon_index = 0
            self.weapon = list(weapon_data.keys())[self.weapon_index]
    
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

        if self.attacking:  # simple attack timer
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()
        
        if self.weapon_changing:
            if (current_time - self.weapon_switch_time >= 
                self.weapon_switch_cooldown):
                self.weapon_changing = False
        

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status += '_idle'
        
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status += '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')
    
    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)