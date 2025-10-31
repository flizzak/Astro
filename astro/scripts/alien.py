import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '''Clase que representa a un solo invasor.'''
    def __init__(self, astro_game):
        '''Inicializando la nave invasora y su posicionamiento en pantalla.'''
        super().__init__()
        self.screen = astro_game.screen
        self.settings = astro_game.settings
        
        # Cargando la imagen de la nave invasora y posicionando la flota.
        self.image = pygame.image.load('D:/astro/imagenes/alien_1.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width + 1050
        self.rect.y = self.rect.height
        
        # Almacenando la posición horizontal de la nave.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
    def update(self):
        """Moviendo naves enemigas hacia la izquierda"""
        self.x -= (self.settings.alien_vel * self.settings.fleet_dirX)
        self.rect.x = self.x
        
    def screenLim(self):
        '''Registramos el valor de True en caso de que alguna de las naves en la flota
        llegue al limite de la pantalla.
        '''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True