import mosaik
from mosaik.util import connect_many_to_one
import networkx as nx
import matplotlib.pyplot as plt


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
END = 25  # seconds of simulation time
N = 2  # number of intersections in each direction


def main():
    world = mosaik.World(SIM_CONFIG)
    create_scenario(world)
    world.run(until=END)
    
    
def create_scenario(world):
    # Start simulators
    intersection_sim = world.start('IntersectionSim')
    road_sim = world.start('RoadSim')
    collector = world.start('Collector')
    
    # Instantiate models
    grid = instantiate_intersection_graph(N)
    intersections = instantiate_intersections(grid, intersection_sim)
    roads = instantiate_roads(world, grid, road_sim)
    monitor = collector.Monitor()
    
    # Connect entities
    connect_many_to_one(world, intersections, monitor, 'traffic_lights')
    
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


def instantiate_roads(world, grid, road_sim):
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
        
        new_road = road_sim.RoadModel(from_direction=from_direction)
        grid.edges[u, v, 0]['road'] = new_road
        roads.append(new_road)
        
        # connect the road to the corresponding intersection
        intersection = grid.nodes[v]['intersection']
        world.connect(intersection, new_road, ('traffic_lights', 'traffic_lights_in'))
    return roads


# Function to draw the graph of intersections and roads
def draw_graph(grid):
    plt.figure(figsize=(8, 8), frameon=False)
    pos = {(x,y):(y,-x) for x,y in grid.nodes()}
    nx.draw_networkx_nodes(grid, pos=pos, node_color='lightgreen', node_size=600)
    for (u, v) in grid.edges():
        nx.draw_networkx_edges(grid, pos=pos, edgelist=[(u, v)], width=2, arrowsize=20, edge_color='blue', connectionstyle='arc3, rad=0.1')
        nx.draw_networkx_edges(grid, pos=pos, edgelist=[(v, u)], width=2, arrowsize=20, edge_color='red', connectionstyle='arc3, rad=0.1')
    nx.draw_networkx_labels(grid, pos=pos, font_size=8)
    plt.axis('equal')
    plt.savefig('grid.png')


if __name__ == "__main__":
    main()
