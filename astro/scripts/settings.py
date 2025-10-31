class Settings:
    """Administra las configuraciones del juego."""

    def __init__(self):
        # Iniicializando el juego como inactivo.
        self.game_active = False
    
        # Configuracion de pantalla
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0,0,0)

        # Configuracion de nave
        self.nave_vel = 1
        self.opoLimite = 1

        # Municiones
        self.disparo_vel = 1.0
        self.disparo_ancho = 4
        self.disparo_alto = 2
        self.disparo_color = (255,255,255)
        self.num_disparos = 100
        
        # Configuracion de miniNaves
        self.alien_vel = 1.0
        self.fleet_vel = 1
        # Configurando direccion de mininaves
        self.fleet_dirX = 1
        self.fleet_dirY = 0