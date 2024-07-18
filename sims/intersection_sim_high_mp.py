import os
import random
import signal
import mosaik_api_v3
import models.intersection_model as intersection_model
from multiprocessing import Pool, cpu_count, Event

META = {
    "type": "time-based",
    "models": {
        "IntersectionModel": {
            "public": True,
            "params": [],
            "attrs": ["traffic_lights"],
        },
    },
}

class IntersectionSim(mosaik_api_v3.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid_prefix = "Intersection_"
        self.entities = {}
        self.time = 0
        self.process_pool = Pool(cpu_count())
        self.shutdown_event = Event()
        self.setup_signal_handler()
        
    def setup_signal_handler(self):
        signal.signal(signal.SIGINT, self.graceful_shutdown)
        signal.signal(signal.SIGTERM, self.graceful_shutdown)
        
    def graceful_shutdown(self, signum, frame):
        print("Received signal to shut down. Shutting down process pool.")
        self.shutdown_event.set()
        self.process_pool.terminate()
        self.process_pool.join()
        print("Process pool shut down gracefully.")
        exit(0)

    def init(self, sid, time_resolution):
        if time_resolution != 1:
            raise ValueError("IntersectionSim only supports time_resolution=1., but %s was set." % time_resolution)
        return self.meta

    def create(self, num, model):
        n_entities = len(self.entities)
        entities = []

        for i in range(n_entities, n_entities + num):
            eid = "%s%d" % (self.eid_prefix, i)
            model_instance = intersection_model.IntersectionModel(eid)
            self.entities[eid] = model_instance
            entities.append({"eid": eid, "type": model})

        return entities

    def step(self, time, inputs, max_advance):
        self.time = time

        _ = self.process_pool.map(estimate_pi, [5000] * 10)

        for eid, model_instance in self.entities.items():
            model_instance.step(time)
        return time + 1

    def get_data(self, outputs):
        data = {}
        for eid, attrs in outputs.items():
            model = self.entities[eid]
            data["time"] = self.time
            data[eid] = {}
            for attr in attrs:
                if attr not in self.meta["models"]["IntersectionModel"]["attrs"]:
                    raise ValueError("Unknown output attribute: %s" % attr)
                data[eid][attr] = getattr(model, attr)
        return data
    
    def finalize(self):
        self.process_pool.close()
        self.process_pool.join()
        
    
def estimate_pi(num_samples=5000):
    inside_circle = 0
    
    for _ in range(num_samples):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x**2 + y**2 <= 1:
            inside_circle += 1
    
    pi_estimate = (inside_circle / num_samples) * 4
    return pi_estimate


def main():
    return mosaik_api_v3.start_simulation(IntersectionSim())


if __name__ == "__main__":
    main()
