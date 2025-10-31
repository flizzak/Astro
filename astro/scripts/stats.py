class PlayerStats:
	''' Capturando las estadisticas del juego '''
    
    def __init__(self,astro_game):
        self.settings  = astro_game.settings
        self.reset_stats()

    def reset_stats(self):
        '''Inicializando las estadisticas'''
        self.oportunidades = self.settings.opoLimit
    