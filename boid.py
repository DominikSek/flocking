import numpy as np
import random
import pygame
from rules import *

class Boids:
    def __init__(self, game_settings, rules, n_boids=25):
        self.game_settings = game_settings
        self.rules = rules
        self.boids = self.init_boids(n_boids)
        
        
    
    def init_boids(self, n):
        boids = []
        for _ in range(n):
            boid = Boid(
                pos=np.array([random.uniform(0, self.game_settings.screen_width), 
                              random.uniform(0, self.game_settings.screen_height)]),
                game_settings = self.game_settings,
                flock=self,
                rules = self.rules
            )
            
            boids.append(boid)
        
        return np.array(boids)

    def local_boids(self, boid):
        return np.array([other_boid for other_boid in self.boids
                         if boid.distance_to(other_boid) < boid.vision_radius and boid != other_boid])
        

class Boid:
    def __init__(self, pos, game_settings, flock, rules, speed=2):
        self.position = pos
        self.game_settings = game_settings
        
        self.max_velocity = game_settings.max_velocity
        self.size = game_settings.boid_radius
        
        self.color = game_settings.boid_color
        self.v = np.array([0, 0])
        self.speed = speed
        
        self.vision_radius = game_settings.vision_radius
        self.flock = flock
        self.rules = rules
        
    def apply_damping(self):
        damping_factor = 0.99  # Adjust as needed
        self.v *= damping_factor
    
    def set_speed(self, v):
        magnitude = np.linalg.norm(v)
        
        if magnitude > self.max_velocity:
            v = v * (self.max_velocity / magnitude)
        
        self.v = v
    
    
    def map_color(self):
        
        magnitude = np.linalg.norm(self.v)
        min_speed = 0
        max_speed = self.max_velocity
        
        color_stops = [
            (0, (0, 255, 0)), 
            (1.0, (0, 255, 255))    
        ]
        
        normalized_speed = (magnitude - min_speed) / (max_speed - min_speed)
        normalized_speed =  max(0, min(normalized_speed, 1))
        
        for i in range(len(color_stops) - 1):
            if color_stops[i][0] <= normalized_speed <= color_stops[i + 1][0]:
                ratio = (normalized_speed - color_stops[i][0]) / (color_stops[i + 1][0] - color_stops[i][0])
                color_start = np.array(color_stops[i][1])
                color_end = np.array(color_stops[i + 1][1])
                color = (color_start * (1 - ratio) + color_end * ratio).astype(int)
                
        self.color = color
        
    def calculate_rules(self, local_boids):
        return sum(
            [rule.evaluate(self, local_boids) * rule.weight for rule in self.rules]
        )
        
    def update_position(self):
        
        local_positions = self.flock.local_boids(self)
        direction = self.calculate_rules(local_positions)
        
        
        self.set_speed(self.v + direction * self.speed)
        #self.apply_damping()
        
        self.position += self.v.astype(int)
        
        self.position[0] = self.position[0] % self.game_settings.map_width
        self.position[1] = self.position[1] % self.game_settings.map_height
        
    
    def distance_to(self, other_boid):
        return np.linalg.norm(self.position - other_boid.position)
    
    
    def draw(self, screen):
        
        self.map_color()
        
        if abs(self.v).sum() == 0:
            direction = np.array([1, 0])
        else:
            direction = self.v / np.linalg.norm(self.v)
        
        direction *= self.size
        perpendicular_direction = np.cross(np.array([*direction, 0]), np.array([0, 0, 1]))[:2]

        centre = self.position

        points = np.array([
            0.5*direction + centre,
            -0.5*direction + 0.33*perpendicular_direction + centre,
            -0.5*direction + centre,
            -0.5*direction - 0.33*perpendicular_direction + centre,
        ])
        
        ## The boid
        pygame.draw.polygon(screen, self.color, points.astype(int)) 
        
        ## The vision radius
        pygame.draw.circle(screen, (150, 150, 150), self.position, self.vision_radius, width=1)

    
    def __str__(self):
        return f"({self.position[0]}, {self.position[1]})"
        
        