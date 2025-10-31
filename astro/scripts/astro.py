import sys
import time
import pygame
from settings import Settings
from PlyStats import GameStats
from nave import Nave
from disparo import Bala
from alien import Alien
from button import Button

class Invasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("Astro")
        
        # Iniciando las estadisticas del juego.
        self.stats = GameStats(self)
        
        # Inicializando la nave, disparos y la flota de aliens a derribar.
        self.nave = Nave(self)
        self.disparos = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        
        # Status del juego.
        self.game_active = True
        
        # Insertando el boton de inicio
        self.play_button = Button(self, "Inicia")
        
        

    def inicia_juego(self):
        while True:
            self._check_events()
            if self.stats.game_active:
                self.nave.update()
                self._update_disparos()
                self._update_aliens()
                self.disparos.update()
                
            self._update_screen()
            

    def _update_aliens(self):
        self._check_screenLim()
        self.aliens.update()
        
        # Colisiones
        if pygame.sprite.spritecollideany(self.nave, self.aliens):
            self._nave_alien()
            
        # Extremo izquierdo
        self._check_alien_izq()
                  
    
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    
    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.stats.reset_stats()
  
            # Limpiando pantalla
            self.aliens.empty()
            self.disparos.empty()
            
            # Inicializando el juego.
            self._create_fleet()
            self.nave.centrado()
            
            # Ocultando el puntero
            pygame.mouse.set_visible(False)

    def _dispara(self):
        if len(self.disparos) < self.settings.num_disparos:
            disparoN = Bala(self)
            self.disparos.add(disparoN)
    
    def _check_screenLim(self):
        for alien in self.aliens.sprites():
            if alien.screenLim():
                self._cambiaDir()
                break
    
    def _cambiaDir(self):
        for alien in self.aliens.sprites():
            alien.rect.x += self.settings.fleet_vel
        self.settings.fleet_dirX *= -1
    
    def _create_fleet(self):
        '''Creando la flote de naves invasoras'''
        # Creando una nave nueva
        alien = Alien(self)
        alien_height, alien_width = alien.rect.size
        nave_ancho = self.nave.rect.width
        espacio_x = (self.settings.screen_width - (3*alien_width) - nave_ancho)
        espacio_y = self.settings.screen_height - (3*alien_height)
        numero_aliens_y = ((espacio_y // (1*alien_height)))+2
        num_regs = espacio_y // (2 * alien_width) 

        
        for col in range(num_regs):
            for alien_num in range(numero_aliens_y):
                self._crea_alien(alien_num,col)
        alien.dx = 0
                
    def _crea_alien(self,alien_num,col_num):
        # Crea una nave invasora y la posiciona en una columna.
        alien = Alien(self)
        alien_height,alien_width = alien.rect.size
        alien.y = alien_height + 1 * alien_height * alien_num
        alien.rect.y = alien.y
        alien.rect.x = (alien.rect.width + 2 * alien.rect.width * col_num) 
        self.aliens.add(alien)
    
    def _check_alien_izq(self):
        '''Revisa cuando los aliens invasores llegan al extremo izquierdo de la pantalla.'''
        screen.rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.left >= self.rect.left:
                self._nave_alien()
                break
    
    
    def _check_keydown_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.nave.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.nave.moving_left = True
        elif event.key == pygame.K_UP:
            self.nave.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.nave.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._dispara()

    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.nave.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.nave.moving_left = False
        elif event.key == pygame.K_UP:
            self.nave.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.nave.moving_down = False
        

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.nave.blitme()
        for bala in self.disparos.sprites():
            bala.dispara()
        self.aliens.draw(self.screen)
        
        # Presenta el boton de inicio en caso de que el juego este inactivo.
        if not self.stats.game_active:
            self.play_button.draw_button()
        
        pygame.display.flip()

    def _update_disparos(self):
        # Eliminando disparos fuera de pantalla
        for bala in self.disparos.copy():
            if bala.rect.right > 1200:
                self.disparos.remove(bala)
        self._check_BalaAlien()
        
    def _check_BalaAlien(self):
        # Revisando colisiones de bala con el alien.
        colision = pygame.sprite.groupcollide(self.disparos, self.aliens, True, True)
        if not self.aliens:
            self.disparos.empty()
            # Aqui metemos al boss.
            print('Nivel terminado')
            self._create_fleet()
        
    def _nave_alien(self):
        '''Midiendo las colisiones de la nave con los aliens'''
        print('Choque')
        
        if self.stats.oportunidades > 0:
            # Reduciendo el numero de naves disponibles.
            self.stats.oportunidades -= 1
            
            # Limpiando pantalla
            self.aliens.empty()
            self.nave.centrado()
            self.disparos.empty()
            
            # Pausa
            time.sleep(1)
        else:
            self.stats.game_active = False
            #pygame.mouse.set_visible(True)
    
            
if __name__ == '__main__':
    astro = Invasion()
    astro.inicia_juego()
