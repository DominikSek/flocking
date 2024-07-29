import numpy as np


class BoidRule:
    def __init__(self, weight, game_settings):
        self.weight = weight
        self.game_settings = game_settings
        
    
    def evaluate(self, boid, local_boids):
        pass
    
    def set_weight(self, weight):
        self.weight = weight


class SeparationRule(BoidRule):
    def __init__(self, *args, push_force=5, **kwargs):
        super().__init__(*args, **kwargs)
        self.push_force = push_force
    
    def evaluate(self, boid, local_boids):
        n = len(local_boids)
        
        if n >= 1:
            directions = np.array([(boid.position - other.position) for other in local_boids])
            distances = np.linalg.norm(directions, axis=1)
            distances = np.clip(distances, 1e-5, None)
            
            separation_vectors = (directions / distances[:, np.newaxis]) * (self.push_force/distances)[:, np.newaxis]
            return np.sum(separation_vectors)
        else:
            return np.array([0, 0])
    

class CohesionRule(BoidRule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def evaluate(self, boid, local_boids):
        if len(local_boids) == 0:
            return np.array([0, 0])

        average_position = np.mean([other_boid.position for other_boid in local_boids])
        difference = average_position- boid.position
        
        norm = np.linalg.norm(difference)
        
        if norm == 0:
            return np.array([0, 0])
        
        return difference / norm
    

class AlignmentRule(BoidRule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def evaluate(self, boid, local_boids):
        other_velocities = np.array([b.v for b in local_boids])

        if len(other_velocities) == 0:
            return np.array([0, 0])

        magnitudes = np.linalg.norm(other_velocities, axis=1, keepdims=True)
        normed_directions = other_velocities / np.clip(magnitudes, a_min=1e-5, a_max=None)

        average_direction = normed_directions.mean(axis=0)
        
        return average_direction