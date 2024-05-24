import mosaik
import mosaik.util
import networkx as nx
import matplotlib.pyplot as plt
import random
import itertools as it
import sys
import time
import psutil

SIM_CONFIG = {
    'IntersectionSim': {
        'python': 'sims.intersection_sim:IntersectionSim',
    },
    'RoadSim': {
        'python': 'sims.road_sim:RoadSim', 
    },
    'Collector': {
        'cmd': '%(python)s sims/collector.py %(addr)s',
    },
}
END = 50                        # seconds of simulation time
MAX_VEHICLES_PER_ROAD = 2       # maximum number of vehicles per road


def main():
    if len(sys.argv) > 1:
        n_intersections_per_side = int(sys.argv[1])
    else:
        raise ValueError('To run the simulation, provide the number of intersections per side as a command line argument')
    
    if n_intersections_per_side < 2:
        raise ValueError('The number of intersections per side must be at least 2')
    
    psutil.cpu_percent(interval=None)
    
    start_tot_time = time.time()
    world = mosaik.World(SIM_CONFIG)
    setup_time = create_scenario(world, n_intersections_per_side)
    world.run(until=END)
    end_tot_time = time.time()
    exec_time = end_tot_time - start_tot_time
    sim_time = exec_time - setup_time
    
    cpu_utilization = psutil.cpu_percent(interval=None)
    per_core_cpu = psutil.cpu_percent(percpu=True)
    mem_utilization = psutil.virtual_memory().percent

    with open('data/multithreading_statistics.txt', 'w') as file:
        file.write(f"Number of intersections: {n_intersections_per_side**2}\n")
        file.write(f"Setup time: {setup_time:.3f} seconds\n")
        file.write(f"Simulation time: {sim_time:.3f} seconds\n")
        file.write(f"Total execution time: {exec_time:.3f} seconds\n")
        file.write(f"CPU utilization: {cpu_utilization:.2f}%\n")
        file.write(f"Per-core CPU utilization: {per_core_cpu}%\n")
        file.write(f"Memory utilization: {mem_utilization:.2f}%\n")
    
    
def create_scenario(world, n_intersections_per_side):
    
    start_init_time = time.time()
    
    # start simulators
    intersection_sim = world.start('IntersectionSim')
    road_sim = world.start('RoadSim')
    collector = world.start('Collector')
    
    # instantiate models
    grid = instantiate_intersection_graph(n_intersections_per_side)
    intersections = instantiate_intersections(grid, intersection_sim)
    roads, adjacency_map = instantiate_roads(world, grid, road_sim)
    
    road_sim.initialize_road_adjacencies(adjacency_map)
    
    monitor = collector.Monitor()
    
    # connect entities
    mosaik.util.connect_many_to_one(world, intersections, monitor, 'traffic_lights')
    mosaik.util.connect_many_to_one(world, roads, monitor, 'num_vehicles')
    
    # draw the intersection graph
    draw_graph(grid)
    
    end_init_time = time.time()
    return end_init_time - start_init_time


def instantiate_intersection_graph(num_intersections):
    grid = nx.grid_2d_graph(num_intersections, num_intersections, create_using=nx.MultiDiGraph())
    return grid


def instantiate_intersections(grid, intersection_sim):
    intersections = []
    
    # TODO: introduce scalability
    for node in grid.nodes():
        new_intersection = intersection_sim.IntersectionModel()
        grid.nodes[node]['intersection'] = new_intersection
        grid.nodes[node]['label'] = new_intersection.eid
        intersections.append(new_intersection)
    return intersections


def instantiate_roads(world, grid, road_sim):
    roads = []
    adjacency_map = {}  # maps road EIDs to lists of adjacent road EIDs
    
    # TODO: introduce scalability
    for u, v, data in grid.edges(data=True):
        road_direction = determine_direction(u, v)      # determine the direction from which of the road is coming
        num_vehicles = random.randint(0, MAX_VEHICLES_PER_ROAD)     # instantiate a random number of vehicles between 0 and MAX for each road
        new_road = road_sim.RoadModel(direction=road_direction, num_vehicles=num_vehicles)
        grid.edges[u, v, 0]['road'] = new_road
        grid.edges[u, v, 0]['label'] = new_road.eid
        roads.append(new_road)
        dest_intersection = grid.nodes[v]['intersection']   # get the destination intersection
        world.connect(dest_intersection, new_road, ('traffic_lights', 'traffic_lights_in'))   # connect the road to the corresponding destination intersection
    
    # create the adjacency map for each road to know the next road in each direction
    for u, v, data in grid.edges(data=True):
        current_direction = determine_direction(u, v)
        eid = grid.edges[u, v, 0]['label']
        adjacency_list = []
        for w in grid.successors(v):
            if w != u:
                adj_direction = determine_direction(v, w)
                relative_direction = calculate_relative_direction(current_direction, adj_direction)
                adj_eid = grid.edges[v, w, 0]['label']
                adjacency_list.append({'road': adj_eid, 'direction': relative_direction})
        adjacency_map[eid] = adjacency_list
    return roads, adjacency_map


def determine_direction(u, v):
    if u[0] < v[0]:
        return 'south'
    elif u[0] > v[0]:
        return 'north'
    elif u[1] < v[1]:
        return 'east' 
    elif u[1] > v[1]:
        return 'west' 
    
    
def calculate_relative_direction(current_direction, adj_direction):
    directions = ['north', 'east', 'south', 'west']
    idx_current = directions.index(current_direction)
    idx_adj = directions.index(adj_direction)
    relative_idx = (idx_adj - idx_current) % 4
    if relative_idx == 1:
        return 'right'
    elif relative_idx == 3:
        return 'left'
    else:
        return 'straight'


def draw_graph(grid):
    plt.figure(figsize=(8, 8), frameon=False)
    pos = {(x,y):(y,-x) for x,y in grid.nodes()} 
    connectionstyle = [f"arc3,rad={r}" for r in it.accumulate([0.15] * 4)]
    
    nx.draw_networkx_nodes(grid, pos, node_color='lightgreen', node_size=600)
    # draw node labels
    node_labels = {node: grid.nodes[node]['label'] for node in grid.nodes()}
    nx.draw_networkx_labels(grid, pos=pos, labels=node_labels, font_size=8)
    
    nx.draw_networkx_edges(grid, pos=pos, edge_color="grey", arrowsize=20, connectionstyle=connectionstyle)
    
    # draw edge labels
    edge_labels = {
        tuple(edge): f"{attrs['label']}"
        for *edge, attrs in grid.edges(keys=True, data=True)
    }
    nx.draw_networkx_edge_labels(
        grid,
        pos=pos,
        edge_labels=edge_labels,
        connectionstyle=connectionstyle,
        label_pos=0.3,
        font_size=8,
        font_color='blue',
        bbox={"alpha": 0}
    )
    plt.axis('equal')
    plt.savefig('images/grid.png')
    nx.drawing.nx_pydot.write_dot(grid, 'images/graph.dot')


if __name__ == '__main__':
    main()