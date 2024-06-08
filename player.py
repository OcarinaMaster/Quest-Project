import pygame
from settings import *
from support import import_folder
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups,obstacle_sprites,create_attack,destroy_weapon):
        super().__init__(groups)
        self.image = pygame.image.load(r".\05 - level graphics\animations\down_idle\tile000.png").convert_alpha()
        self.height = self.image.get_height
        self.width = self.image.get_width
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-40)
        #graphic setup
        self.import_player_assets()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15
        #movement
        self.obstacle_sprites = obstacle_sprites
        self.attacking = False
        self.attack_cooldown =400
        self.attack_time = 0
        
        self.direction =  pygame.math.Vector2()
        #attack
        self.create_attack = create_attack
        self.destroy_weapon = destroy_weapon
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        
        #stats
        self.stats = {'health':100, 'attack':10, 'speed':6}
        self.health = self.stats['health']
        self.exp =  123
        self.speed = self.stats['speed']
    def get_status(self):
        #idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status += '_idle'
        if self.attacking:
            self.direction.x=0
            self.direction.y=0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle','_attack')
                else:
                    self.status += '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack','') 
    
    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
            
        #set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)
            
    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()
            
            #basic movement
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
                #self.rect.y -= self.speed
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
                #self.rect.y += self.speed
            #makes sure that the player doesnt keep going in one direction, and once key is lifted it stops
            else:
                self.direction.y  = 0
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
                #self.rect.x += self.speed
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
                #self.rect.x -= self.speed
            else:
                self.direction.x = 0
            
            #attack input
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                
        
    def import_player_assets(self):
        character_path = r'05 - level graphics\animations'
        self.animations = {'up': [], 'down':[], 'left':[],'right': [],
                        'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
                        'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]}
        for animation in self.animations.keys():
            full_path = character_path+"/"+animation
            self.animations[animation] = import_folder(full_path)
        print(self.animations)
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_weapon()
    
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
        self.cooldowns()
        self.get_status()
        self.animate()
        self.collision(self.direction)