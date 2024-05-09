import json

class VehicleModel:
    """
    Class to represent a simple vehicle model that get directions from a JSON file
    """
    def __init__(self, directions_file):
        # Load directions from JSON file
        with open(directions_file, 'r') as f:
            self.directions = json.load(f)

        self.current_road = None
        self.state = 'waiting'  # waiting / moving / finished

    def step(self):
        # TODO: vehicle behavior for each simulation step
        pass

    def update_state(self, new_state):
        self.state = new_state

    def update_position(self, new_road):
        self.current_road = new_road
