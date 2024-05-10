import mosaik
from mosaik.util import connect_many_to_one
import networkx as nx
import matplotlib.pyplot as plt
import random
import json

SIM_CONFIG = {
    'IntersectionSim': {
        'python': 'sims.intersection_sim:IntersectionSim',
    },
    'RoadSim': {
        'python': 'sims.road_sim:RoadSim', 
    },
    'VehicleSim': {
        'python': 'sims.vehicle_sim:VehicleSim',
    },
    'Collector': {
        'cmd': '%(python)s sims/collector.py %(addr)s',
    },
}
END = 25                    # seconds of simulation time
INTERSECTIONS_PER_SIDE = 2  # number of intersections in each direction of the square grid
MAX_VEHICLES_PER_ROAD = 10   # maximum number of vehicles per road


def main():
    world = mosaik.World(SIM_CONFIG)
    create_scenario(world)
    world.run(until=END)
    
    
def create_scenario(world):
    
    # Start simulators
    intersection_sim = world.start('IntersectionSim')
    road_sim = world.start('RoadSim')
    vehicle_sim = world.start('VehicleSim')
    collector = world.start('Collector')
    
    tot_vehicles = 0
    
    # Instantiate models
    grid = instantiate_intersection_graph(INTERSECTIONS_PER_SIDE)
    intersections = instantiate_intersections(grid, intersection_sim)
    roads, tot_vehicles = instantiate_roads(world, grid, road_sim, tot_vehicles)
    
    generate_directions_file(tot_vehicles)
    vehicles = instantiate_vehicles(world, roads, vehicle_sim)
    
    monitor = collector.Monitor()
    
    # Connect entities
    connect_many_to_one(world, intersections, monitor, 'traffic_lights')
    connect_many_to_one(world, roads, monitor, 'num_vehicles')
    
    # Draw the intersection graph
    draw_graph(grid)


def instantiate_intersection_graph(num_intersections):
    grid = nx.grid_2d_graph(num_intersections, num_intersections, create_using=nx.MultiDiGraph())
    return grid


def instantiate_intersections(grid, intersection_sim):
    intersections = []
    for node in grid.nodes():
        new_intersection = intersection_sim.IntersectionModel()
        grid.nodes[node]['intersection'] = new_intersection
        intersections.append(new_intersection)
    return intersections


def instantiate_roads(world, grid, road_sim, tot_vehicles):
    roads = []
    
    for u, v, data in grid.edges(data=True):
        # get direction from which the road comes from based on the position of the nodes
        from_direction = ''
        if u[0] < v[0]:
            from_direction = 'north'
        elif u[0] > v[0]:
            from_direction = 'south'
        elif u[1] < v[1]:
            from_direction = 'west'
        elif u[1] > v[1]:
            from_direction = 'east'
        
        # instantiate a random number of vehicles between 0 and 5 for each road
        num_vehicles = random.randint(1, MAX_VEHICLES_PER_ROAD)
        tot_vehicles += num_vehicles
        
        new_road = road_sim.RoadModel(from_direction=from_direction, num_vehicles=num_vehicles)
        grid.edges[u, v, 0]['road'] = new_road
        roads.append(new_road)
        
        # connect the road to the corresponding destination intersection
        intersection = grid.nodes[v]['intersection']
        world.connect(intersection, new_road, ('traffic_lights', 'traffic_lights_in'))
        
    return roads, tot_vehicles
    

def instantiate_vehicles(world, roads, vehicle_sim):
    vehicles = []
    
    data = world.get_data(roads, 'num_vehicles')
    for road in roads:
        road_id = int(road.eid.split('_')[1])
        num_vehicles = data[roads[road_id]]['num_vehicles']
        vehicles.extend(vehicle_sim.VehicleModel.create(num_vehicles, init_road=road.eid))
        
    return vehicles
    

def draw_graph(grid):
    plt.figure(figsize=(8, 8), frameon=False)
    pos = {(x,y):(y,-x) for x,y in grid.nodes()}
    nx.draw_networkx_nodes(grid, pos=pos, node_color='lightgreen', node_size=600)
    for (u, v) in grid.edges():
        nx.draw_networkx_edges(grid, pos=pos, edgelist=[(u, v)], width=2, arrowsize=20, edge_color='blue', connectionstyle='arc3, rad=0.1')
        nx.draw_networkx_edges(grid, pos=pos, edgelist=[(v, u)], width=2, arrowsize=20, edge_color='red', connectionstyle='arc3, rad=0.1')
    nx.draw_networkx_labels(grid, pos=pos, font_size=8)
    plt.axis('equal')
    plt.savefig('images/grid.png')
    

def generate_directions_file(tot_vehicles):
    directions = {}
    
    for i in range(tot_vehicles):
        vehicle_id = 'Vehicle_' + str(i)
        directions[vehicle_id] = [random.choice(['straight', 'left', 'right']) for _ in range(5)]

    with open('data/directions.json', 'w') as f:
        json.dump(directions, f)


if __name__ == "__main__":
    main()
