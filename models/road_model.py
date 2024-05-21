import models.vehicle_model as vehicle_model


class RoadModel:
    def __init__(self, eid, direction, num_vehicles, vehicles_count):
        self.eid = eid
        self.direction = direction              # direction of the road, which indicates the right intersection traffic light to monitor
        self.num_vehicles = num_vehicles        # number of vehicles on the road at the beginning of the simulation
        self.next_adjacent_roads = []           # list of roads going to the next intersections
        self.vehicle_queue = []
        for i in range(vehicles_count, vehicles_count + num_vehicles):
            self.vehicle_queue.append(vehicle_model.VehicleModel(self.eid, i))
    
    def __str__(self):
        if len(self.vehicle_queue) > 0:
            vehicles_info = ",\n\t\t\t".join(str(vehicle) for vehicle in self.vehicle_queue)
            vehicle_str = f"\n\t\t\t{vehicles_info}\n\t\t"
        else:
            vehicle_str = ""
        adjacent_roads = ", ".join(str(road['direction'] + ': ' + road['road'].eid) for road in self.next_adjacent_roads)
        return f"{self.eid}:\n\t\tdir={self.direction},\n\t\tnum_vehicles={self.num_vehicles},\n\t\tvehicles_queue=[{vehicle_str}],\n\t\tadjacent_roads=[{adjacent_roads}]"

    def step(self, traffic_lights_in):
        tl_direction = self.determine_traffic_light_direction()
        if traffic_lights_in[tl_direction] == 'green' and len(self.vehicle_queue) > 0:
            vehicle = self.remove_vehicle()                     # remove vehicle from this road's queue
            next_direction = vehicle.get_next_direction()       # get next vehicle direction ('left', 'right', 'straight')
            
            # if there is a next direction, transfer the vehicle to the next road
            if next_direction is not None:
                next_road = self.get_road_by_direction(next_direction)
                if next_road is not None:
                    self.transfer_vehicle(vehicle, next_road)
                else:
                    # if the road in a direction does not exist, remove the vehicle from the simulation
                    # print(f"{vehicle.eid} is trying to move to a non-existing road. RIP...")
                    del vehicle
            else:
                # there is no next direction, the vehicle has arrived at its destination
                # print(f"{vehicle.eid} has arrived at its destination. YAY!")
                del vehicle
            
    def determine_traffic_light_direction(self):
        if self.direction == 'north':
            return 'south'
        elif self.direction == 'south':
            return 'north'
        elif self.direction == 'east':
            return 'west'
        elif self.direction == 'west':
            return 'east'
        else:
            return None
            
    def add_vehicle(self, vehicle):
        self.vehicle_queue.append(vehicle)
        self.num_vehicles += 1
        
    def remove_vehicle(self):
        self.num_vehicles -= 1
        return self.vehicle_queue.pop(0)
    
    def transfer_vehicle(self, vehicle, target_road):
        target_road.add_vehicle(vehicle)
        vehicle.update_position(target_road.eid)

    def get_road_by_direction(self, direction):
        for adjacent_road in self.next_adjacent_roads:
            if adjacent_road['direction'] == direction:
                return adjacent_road['road']
        return None
    