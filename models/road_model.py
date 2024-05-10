class RoadModel:
    """
    Class to represent a simple road model that manages a queue of vehicles
    """
    def __init__(self, from_direction, num_vehicles=0):
        self.from_direction = from_direction
        self.num_vehicles = num_vehicles

    def step(self, traffic_lights_in):
        if traffic_lights_in[self.from_direction] == 'green' and self.num_vehicles > 0:
            self.num_vehicles -= 1
