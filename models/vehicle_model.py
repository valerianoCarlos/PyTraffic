import random

N_DIRECTIONS_PER_VEHICLE = 10


class VehicleModel:
    def __init__(self, init_road, id):
        self.eid = f"Vehicle_{id}"
        self.directions = [random.choice(["straight", "left", "right"]) for _ in range(N_DIRECTIONS_PER_VEHICLE)]
        self.curr_road = init_road   # eid of the road in which the vehicle is currently located
        self.arrived = False
        
    def __str__(self):
        return f"{self.eid}: current_road='{self.curr_road}', directions='{self.directions}', arrived='{self.arrived}'"

    def update_position(self, new_road):
        self.curr_road = new_road
        
    def get_next_direction(self):
        if self.directions:
            next_dir = self.directions.pop(0)
            if len(self.directions) == 0:
                self.arrived = True
            return next_dir
        else:
            return None
