import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups,obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(r".\animations\down_idle\tile000.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-40)
        self.speed = 5
        self.obstacle_sprites = obstacle_sprites
        self.direction =  pygame.math.Vector2()
    
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.direction.y = -1
            #self.rect.y -= self.speed
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            #self.rect.y += self.speed
        #makes sure that the player doesnt keep going in one direction, and once key is lifted it stops
        else:
            self.direction.y  = 0
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            #self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            #self.rect.x -= self.speed
        else:
            self.direction.x = 0
        
    def move(self, speed):
        #The magnitude function is essentially the hypotenuse, and if its not 0 we want to normalize it(if theres both an
        # x or y value)
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center
        #self.rect.center += self.direction * speed
    
    def collision(self,direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: #moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: #moving left
                        self.hitbox.left = sprite.hitbox.right
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: #moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y< 0: # moving up
                        self.hitbox.top = sprite.hitbox.bottom
    def update(self):
        self.input()
        self.move(self.speed)
        self.collision(self.direction)