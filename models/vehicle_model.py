import json

DIRS_FILE = 'data/directions.json'


class VehicleModel:
    def __init__(self, init_road, id):
        self.eid = f'Vehicle_{id}'

        # load directions from JSON file
        with open(DIRS_FILE) as file:
            all_directions = json.load(file)
        
        self.directions = all_directions.get(self.eid, [])  # list of directions for the vehicle
        self.curr_road = init_road   # eid of the road in which the vehicle is currently located
        
    def __str__(self):
        return f"{self.eid}: current_road='{self.curr_road}', directions='{self.directions}'"

    def update_position(self, new_road):
        self.curr_road = new_road
        
    def get_next_direction(self):
        if self.directions:
            return self.directions.pop(0)
        else:
            return None
