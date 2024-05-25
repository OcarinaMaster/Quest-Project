import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
class Level:
    def __init__(self):
        
        #gets display surface from anywhere in code
        
        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obastacle_sprites = pygame.sprite.Group()
        #sprite setup
        self.create_map()
    
    #finds the different positions (Think back to CSA when we did 2D arrays we kinda traverse this the same way)
    def create_map(self):
        for row_index,row in enumerate(WORLD_MAP):
            for col_index,col in enumerate(row):
                x = col_index * TILESIZE #Gives us the x position
                y = row_index * TILESIZE #Gives us the y position
                if col == "x":
                    self.tile = Tile((x,y),[self.visible_sprites, self.obastacle_sprites])
                if col == "p":
                    self.player = Player((x,y),[self.visible_sprites],self.obastacle_sprites)    
                    
    def run(self):
        #update and draw the game
        
        #draws the visible sprites 
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        

#This is to create a custom camera group that sorts objects by y to give it depth
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        #general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] //2
        self.half_height = self.display_surface.get_size()[1] //2
        self.offset = pygame.math.Vector2()
        
        #creating floor
        self.floor_surface = pygame.image.load(r'.\1 - level\graphics\tilemap\ground.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))
    
    def custom_draw(self, player):
        
        #getting offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        #drawing floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface,floor_offset_pos)
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_rect = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_rect)