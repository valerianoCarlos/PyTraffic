class RoadModel:
    """
    Class to represent a simple road model that manages a queue of vehicles
    """
    def __init__(self, from_direction):
        self.from_direction = from_direction
        self.vehicles_queue = []
        
    def __str__(self):
        return f"RoadModel instance with from_direction: {self.from_direction}"

    def add_vehicle(self, vehicle):
        self.vehicles_queue.append(vehicle)

    def step(self, traffic_lights_in):
        print('traffic_lights_in:', traffic_lights_in) # TODO: remove this line
        if traffic_lights_in[self.from_direction] == 'green' and len(self.vehicles_queue) > 0:
            self.vehicles_queue.pop(0)
