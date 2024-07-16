
# Constants used in the project

SIM_CONFIG_NS = {
    "IntersectionSim": {
        "python": "sims.intersection_sim:IntersectionSim",
        "env": { "LOGURU_LEVEL": "INFO" },
    },
    "RoadSim": {
        "python": "sims.road_sim:RoadSim",
        "env": { "LOGURU_LEVEL": "INFO" }, 
    },
    "Collector": {
        "cmd": "%(python)s sims/collector.py %(addr)s",
        "env": { "LOGURU_LEVEL": "INFO" },
    },
}

SIM_CONFIG_MT = {
    "IntersectionSim": {
        "python": "sims.intersection_sim:IntersectionSim",
        "env": { "LOGURU_LEVEL": "INFO" },
    },
    "RoadSim": {
        "python": "sims.road_sim:RoadSim",
        "env": { "LOGURU_LEVEL": "INFO" }, 
    },
    "Collector": {
        "cmd": "%(python)s sims/collector_mt.py %(addr)s",
        "env": { "LOGURU_LEVEL": "INFO" },
    },
}

SIM_CONFIG_MP = {
    "IntersectionSim": {
        "python": "sims.intersection_sim_mp:IntersectionSim",
        "env": { "LOGURU_LEVEL": "INFO" },
    },
    "RoadSim": {
        "python": "sims.road_sim:RoadSim",
        "env": { "LOGURU_LEVEL": "INFO" }, 
    },
    "Collector": {
        "cmd": "%(python)s sims/collector_mt.py %(addr)s",
        "env": { "LOGURU_LEVEL": "INFO" },
    },
}

SIM_CONFIG_RAY = {
    "IntersectionSim": {
        "python": "sims.intersection_sim_ray:IntersectionSim",
        "env": { "LOGURU_LEVEL": "INFO" },
    },
    "RoadSim": {
        "python": "sims.road_sim:RoadSim",
        "env": { "LOGURU_LEVEL": "INFO" }, 
    },
    "Collector": {
        "cmd": "%(python)s sims/collector_mt.py %(addr)s",
        "env": { "LOGURU_LEVEL": "INFO" },
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

N_INTERSECTIONS = "# Intersections"
SETUP_TIME = "Setup time"
SIM_TIME = "Simulation time"
TOT_TIME = "Total execution time"
CPU_USAGE = "CPU usage"
MEM_USAGE = "Memory usage"