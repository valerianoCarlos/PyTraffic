class IntersectionModel:
    def __init__(self):
        self.traffic_lights = {
            'north': 'red',
            'south': 'red',
            'east': 'green',
            'west': 'green'
        }
        self.light_duration = 10    # seconds

    def step(self, time_elapsed):
        if time_elapsed % self.light_duration == 0:
            for direction in self.traffic_lights:
                if self.traffic_lights[direction] == 'green':
                    self.traffic_lights[direction] = 'red'
                elif self.traffic_lights[direction] == 'red':
                    self.traffic_lights[direction] = 'green'
                else:
                    raise ValueError('Invalid traffic light state: %s', self.traffic_lights[direction])
