import json

DIRS_FILE = 'data/directions.json'


class VehicleModel:
    """
    Class to represent a simple vehicle model that get directions from a JSON file
    """
    def __init__(self, init_road, id):
        self.eid = f'Vehicle_{id}'

        # Load directions from JSON file
        with open(DIRS_FILE) as f:
            all_directions = json.load(f)
        
        self.directions = all_directions.get(self.eid, [])
        self.curr_road = init_road
        self.curr_state = 'waiting'  # waiting / moving / finished
        
    def __str__(self):
        return f"Vehicle: ID='{self.eid}', Current Road='{self.curr_road}', State='{self.curr_state}', Directions='{self.directions}'"

    def step(self):
        # TODO: vehicle behavior for each simulation step
        
        # If the vehicle state becomes 'moving'
        # Get a reference to the grid of intersections
        # Look at the next direction to take
        # If the next direction leads to a road, move to that road by updating the current_road attribute
        # If the next direction leads outside the grid, update the state to 'finished'
        
        pass

    def update_state(self, new_state):
        self.curr_state = new_state

    def update_position(self, new_road):
        self.curr_road = new_road
