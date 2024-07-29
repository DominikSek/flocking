import pygame
from rules import *
from utils import GameSettings
from boid import Boids
import numpy as np


VELOCITY_INCREMENT = 1
pygame.init()
clock = pygame.time.Clock()



if __name__ == "__main__":
    
    game_settings = GameSettings()
    
    screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height))
    running = True
    
    rules = [
            SeparationRule(game_settings=game_settings, push_force=25, weight=1),
            CohesionRule(game_settings=game_settings, weight=0.5),
            AlignmentRule(game_settings=game_settings, weight=1)
        ]
    
    boids = Boids(game_settings, rules, n_boids=25)
    
    while game_settings.is_running:

        for e in pygame.event.get():
            
            if e.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            
            elif e.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                velocity = np.array([0., 0.])
                
                if keys[pygame.K_LEFT]:
                    velocity[0] -= VELOCITY_INCREMENT
                if keys[pygame.K_RIGHT]:
                    velocity[0] += VELOCITY_INCREMENT
                if keys[pygame.K_UP]:
                    velocity[1] -= VELOCITY_INCREMENT
                if keys[pygame.K_DOWN]:
                    velocity[1] += VELOCITY_INCREMENT
                boids.boids[0].set_speed(velocity)
                        
        screen.fill(game_settings.background_color)
        
        for boid in boids.boids:
            boid.update_position()
        for boid in boids.boids:
            boid.draw(screen)
            
        
        pygame.display.flip()
        
        clock.tick(game_settings.ticks_per_second)
        
        
        
        