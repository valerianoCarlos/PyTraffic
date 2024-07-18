
# Constants used in the project

SIM_CONFIG_NS = {
    "IntersectionSim": {
        "python": "sims.intersection_sim:IntersectionSim",
    },
    "RoadSim": {
        "python": "sims.road_sim:RoadSim",
    },
    "Collector": {
        "cmd": "%(python)s sims/collector.py %(addr)s",
    },
}

SIM_CONFIG_MT = {
    "IntersectionSim": {
        "python": "sims.intersection_sim:IntersectionSim",
    },
    "RoadSim": {
        "python": "sims.road_sim:RoadSim",
    },
    "Collector": {
        "cmd": "%(python)s sims/collector_mt.py %(addr)s",
    },
}

SIM_CONFIG_MP = {
    "IntersectionSim": {
        "python": "sims.intersection_sim_mp:IntersectionSim",
    },
    "RoadSim": {
        "python": "sims.road_sim:RoadSim",
    },
    "Collector": {
        "cmd": "%(python)s sims/collector_mt.py %(addr)s",
    },
}

SIM_CONFIG_RAY = {
    "IntersectionSim": {
        "python": "sims.intersection_sim_ray:IntersectionSim",
    },
    "RoadSim": {
        "python": "sims.road_sim:RoadSim",
    },
    "Collector": {
        "cmd": "%(python)s sims/collector_mt.py %(addr)s",
    },
}

SIM_CONFIG_NS_HIGH = {
    "IntersectionSim": {
        "python": "sims.intersection_sim_high:IntersectionSim",
    },
    "RoadSim": {
        "python": "sims.road_sim:RoadSim",
    },
    "Collector": {
        "cmd": "%(python)s sims/collector_high.py %(addr)s",
    },
}

SIM_CONFIG_MT_HIGH = {
    "IntersectionSim": {
        "python": "sims.intersection_sim_high_mt:IntersectionSim",
    },
    "RoadSim": {
        "python": "sims.road_sim:RoadSim",
    },
    "Collector": {
        "cmd": "%(python)s sims/collector_high_mt.py %(addr)s",
    },
}

SIM_CONFIG_MP_HIGH = {
    "IntersectionSim": {
        "python": "sims.intersection_sim_high_mp:IntersectionSim",
    },
    "RoadSim": {
        "python": "sims.road_sim:RoadSim",
    },
    "Collector": {
        "cmd": "%(python)s sims/collector_high_mt.py %(addr)s",
    },
}

SIM_CONFIG_RAY_HIGH = {
    "IntersectionSim": {
        "python": "sims.intersection_sim_high_ray:IntersectionSim",
    },
    "RoadSim": {
        "python": "sims.road_sim:RoadSim",
    },
    "Collector": {
        "cmd": "%(python)s sims/collector_high_mt.py %(addr)s",
    },
}


SCALABILITY_MODES = [
    "no_scaling", 
    "multithreading", 
    "multithreading_nogil", 
    "multiprocessing", 
    "ray",
    "no_scaling_high",
    "multithreading_high",
    "multithreading_nogil_high",
    "multiprocessing_high",
    "ray_high"
]

END = 500
MAX_VEHICLES_PER_ROAD = 20
LIGHT_DURATION = 10

N_INTERSECTIONS = "# Intersections"
SETUP_TIME = "Setup time"
SIM_TIME = "Simulation time"
TOT_TIME = "Total execution time"
CPU_USAGE = "CPU usage"
MEM_USAGE = "Memory usage"