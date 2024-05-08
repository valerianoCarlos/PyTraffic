import mosaik
import mosaik.util

# Sim config and other parameters
SIM_CONFIG = {
    'IntersectionSim': {
        'python': 'sims.intersection_sim:IntersectionSim',
    },
    'Collector': {
        'cmd': '%(python)s sims/collector.py %(addr)s',
    },
}
END = 25  # seconds of simulation time
N = 3  # number of intersections in each direction

# Create the world
world = mosaik.World(SIM_CONFIG)

# Start the simulators
intersection_sim = world.start('IntersectionSim')
collector = world.start('Collector')

# Instatiate the simulators
intersections = intersection_sim.IntersectionModel.create(N * N)
monitor = collector.Monitor()

# Connect the entities
mosaik.util.connect_many_to_one(world, intersections, monitor, 'traffic_lights')

# Run the simulation
world.run(until=END)