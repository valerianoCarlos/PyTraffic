import ray
import numpy as np

# ray.init(ignore_reinit_error=True, include_dashboard=False)

LIGHT_DURATION = 10    # seconds

class IntersectionModel:
    def __init__(self, eid):
        self.eid = eid
        self.traffic_lights = {
            'north': 'red',
            'south': 'red',
            'east': 'green',
            'west': 'green'
        }

    def __str__(self):
        return f"IntersectionModel(eid={self.eid}, traffic_lights={self.traffic_lights})"

    def step(self, time_elapsed):
        if time_elapsed % LIGHT_DURATION == 0:
            # simulate a heavy computation
            for _ in range(10):
                heavy_computation.remote()
                
            for direction in self.traffic_lights:
                if self.traffic_lights[direction] == 'green':
                    self.traffic_lights[direction] = 'red'
                elif self.traffic_lights[direction] == 'red':
                    self.traffic_lights[direction] = 'green'
                else:
                    raise ValueError('Invalid traffic light state: %s', self.traffic_lights[direction])


@ray.remote
def heavy_computation(iterations=10000):
    # Monte Carlo integration to estimate the value of Pi
    count_inside = 0
    for _ in range(iterations):
        x, y = np.random.rand(2)
        if x**2 + y**2 <= 1.0:
            count_inside += 1
    
    pi_estimate = (count_inside / iterations) * 4
    return pi_estimate
