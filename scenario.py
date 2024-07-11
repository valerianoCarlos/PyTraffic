import mosaik
import mosaik.util
import networkx as nx
# import matplotlib.pyplot as plt
import random
import itertools as it
import sys
import time
import psutil
import threading

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
END = 500                         # seconds of simulation time
MAX_VEHICLES_PER_ROAD = 20        # maximum number of vehicles per road
SCALABILITY_MODES = ['no_scaling', 'no_scaling_nogil', 'multithreading', 'multithreading_nogil', 'multiprocessing', 'ray']

def main():
    # check input parameters
    if len(sys.argv) == 3:
        n_intersections_per_side = int(sys.argv[1])
        scalability_mode = sys.argv[2]
    else:
        raise ValueError('To run the simulation, provide the number of intersections per side and the scalability mode as command line arguments')
    
    if n_intersections_per_side < 2:
        raise ValueError('The number of intersections per side must be at least 2')
    
    if scalability_mode not in SCALABILITY_MODES:
        raise ValueError('The scalability mode must be one of the following: no_scaling, multithreading, multithreading_nogil, multiprocessing, ray')
    
    # start resource monitoring in a separate thread
    stop_event = threading.Event()
    resource_data = []
    resource_thread = threading.Thread(target=monitor_resources, args=(stop_event, resource_data))
    resource_thread.start()
    
    # start time monitoring
    start_tot_time = time.time()
    
    # run simulation
    world = mosaik.World(SIM_CONFIG)
    grid, setup_time = create_scenario(world, n_intersections_per_side)   
    world.run(until=END)
    stop_event.set()
    
    # stop time monitoring
    end_tot_time = time.time()
    exec_time = end_tot_time - start_tot_time
    sim_time = exec_time - setup_time
    n_roads = len(grid.edges)
    
    # stop resource monitoring
    resource_thread.join()
    avg_memory_usage, avg_cpu_usage = resource_data
    
    # write simulation statistics to a CSV file
    with open(f"data/{scalability_mode}/benchmark_stats_{n_intersections_per_side}.csv", 'w') as file:
        file.write("# Intersections,# Roads,Setup time,Simulation time,Total execution time,CPU usage,Memory usage\n")
        file.write(f"{n_intersections_per_side**2},{n_roads},{setup_time:.2f},{sim_time:.2f},{exec_time:.2f},{avg_cpu_usage:.2f},{avg_memory_usage:.2f}\n")

    
def create_scenario(world, n_intersections_per_side):
    # start time monitoring
    start_init_time = time.time()
    
    # start simulators
    intersection_sim = world.start('IntersectionSim')
    road_sim = world.start('RoadSim')
    collector = world.start('Collector')
    
    # instantiate models
    grid = instantiate_intersection_graph(n_intersections_per_side)
    intersections = instantiate_intersections(grid, intersection_sim)
    roads, adjacency_map = instantiate_roads(world, grid, road_sim)
    monitor = collector.Monitor()
    
    # initialize the road adjacencies
    road_sim.initialize_road_adjacencies(adjacency_map)
    
    # connect entities
    mosaik.util.connect_many_to_one(world, intersections, monitor, 'traffic_lights')
    mosaik.util.connect_many_to_one(world, roads, monitor, 'num_vehicles')
    
    # draw the intersection graph
    # draw_graph(grid)
    
    # stop time monitoring
    end_init_time = time.time()
    init_time = end_init_time - start_init_time
    return grid, init_time


def instantiate_intersection_graph(num_intersections):
    # create a grid graph with num_intersections x num_intersections nodes
    grid = nx.grid_2d_graph(num_intersections, num_intersections, create_using=nx.MultiDiGraph())
    return grid


def instantiate_intersections(grid, intersection_sim):
    intersections = []
    
    for node in grid.nodes():
        new_intersection = intersection_sim.IntersectionModel()
        grid.nodes[node]['intersection'] = new_intersection
        grid.nodes[node]['label'] = new_intersection.eid
        intersections.append(new_intersection)
    return intersections


def instantiate_roads(world, grid, road_sim):
    roads = []
    adjacency_map = {}  # maps road EIDs to lists of adjacent road EIDs
    
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
    
    # draw nodes
    nx.draw_networkx_nodes(grid, pos, node_color='lightgreen', node_size=600)
    
    # draw node labels
    node_labels = {node: grid.nodes[node]['label'] for node in grid.nodes()}
    nx.draw_networkx_labels(grid, pos=pos, labels=node_labels, font_size=8)
    
    # draw edges
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
    
    
def monitor_resources(stop_event, resource_data, interval=.5):
    memory_samples = []
    cpu_samples = []

    try:
        while not stop_event.is_set():
            memory_samples.append(psutil.virtual_memory().percent)
            cpu_samples.append(psutil.cpu_percent(interval=interval))
            time.sleep(interval)
    except KeyboardInterrupt:
        # stop monitoring when interrupted
        pass

    if memory_samples and cpu_samples:
        avg_memory_usage = sum(memory_samples) / len(memory_samples)
        avg_cpu_usage = sum(cpu_samples) / len(cpu_samples)
        resource_data.extend([avg_memory_usage, avg_cpu_usage])
    else:
        resource_data.extend([0, 0])


if __name__ == '__main__':
    main()
