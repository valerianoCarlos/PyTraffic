import random
import mosaik_api_v3
import models.intersection_model as intersection_model

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
        for _ in range(10):
            estimate_pi()
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