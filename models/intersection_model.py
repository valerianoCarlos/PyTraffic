import numpy as np

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
            # simulate a heavy computation
            for _ in range(10):
                heavy_computation()
            for direction in self.traffic_lights:
                if self.traffic_lights[direction] == 'green':
                    self.traffic_lights[direction] = 'red'
                elif self.traffic_lights[direction] == 'red':
                    self.traffic_lights[direction] = 'green'
                else:
                    raise ValueError('Invalid traffic light state: %s', self.traffic_lights[direction])

def heavy_computation(it=1_000):
    count = 0
    rng = np.random.default_rng(seed=42)
    for _ in range(it):
        x, y = rng.random(2)
        if x**2 + y**2 <= 1:
            count += 1
    pi = 4 * count / it
    return pi