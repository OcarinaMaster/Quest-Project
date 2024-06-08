import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)
        direction = player.status.split('_')[0]
        path = r'05 - level graphics\5 - level graphics\graphics\weapons'
        #graphic
        full_path = f'{path}\{player.weapon}\{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()
        
        #placement
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright+pygame.math.Vector2(-6,13))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft+pygame.math.Vector2(6,13))
        elif direction == 'up':
            self.rect = self.image.get_rect(midbottom = player.rect.midtop+pygame.math.Vector2(-13,13))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom+pygame.math.Vector2(13,0))
        
        else:
            self.rect = self.image.get_rect(center = player.rect.center)