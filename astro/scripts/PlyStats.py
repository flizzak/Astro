class GameStats:
    def __init__(self,astro_game):
        self.settings  = astro_game.settings
        self.reset_stats()
        
        ## Inicializando el estado del juego.
        self.game_active = False
        

    def reset_stats(self):
        '''Inicializando las estadisticas'''
        self.oportunidades = self.settings.opoLimite