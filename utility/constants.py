
# Constants used in the project

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

SCALABILITY_MODES = [
    "no_scaling", 
    "multithreading", 
    "multithreading_nogil", 
    "multiprocessing", 
    "ray",
    "heavy_no_scaling",
    "heavy_multithreading",
    "heavy_multithreading_nogil",
    "heavy_multiprocessing",
    "heavy_ray"
]

END = 500
MAX_VEHICLES_PER_ROAD = 20

N_INTERSECTIONS = '# Intersections'
SETUP_TIME = 'Setup time'
SIM_TIME = 'Simulation time'
TOT_TIME = 'Total execution time'
CPU_USAGE = 'CPU usage'
MEM_USAGE = 'Memory usage'