SCREEN_WIDTH = 840
SCREEN_HEIGHT = 470

BACKGROUND_COLOR = (60, 60, 60)
BOID_COLOR = (255, 0, 0)

MAX_VELOCITY = 2
RADIUS = 10
VISION_RADIUS = 60

TICKS_PER_SECOND = 60

MAP_WIDTH = 860
MAP_HEIGHT = 490


class GameSettings:
    
    def __init__(self):
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        
        self.map_width = MAP_WIDTH
        self.map_height = MAP_HEIGHT
        
        self.background_color = BACKGROUND_COLOR
        self.boid_color = BOID_COLOR
        
        self.vision_radius = VISION_RADIUS
        self.boid_radius = RADIUS
        self.max_velocity = MAX_VELOCITY
    
        
        
        self.ticks_per_second = TICKS_PER_SECOND
        self.is_running = True
    