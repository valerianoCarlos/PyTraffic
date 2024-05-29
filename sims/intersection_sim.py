import mosaik_api_v3
import models.intersection_model as intersection_model
import ray

META = {
    'type': 'time-based',
    'models': {
        'IntersectionModel': {
            'public': True,
            'params': [],
            'attrs': ['traffic_lights'],
        },
    },
}


class IntersectionSim(mosaik_api_v3.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid_prefix = 'Intersection_'
        self.entities = {}
        self.time = 0

    def init(self, sid, time_resolution):
        if time_resolution != 1:
            raise ValueError('IntersectionSim only supports time_resolution=1., but %s was set.' % time_resolution)
        return self.meta

    def create(self, num, model):
        n_entities = len(self.entities)
        entities = []

        for i in range(n_entities, n_entities + num):
            eid = '%s%d' % (self.eid_prefix, i)
            model_instance = intersection_model.IntersectionModel.remote(eid=eid)
            self.entities[eid] = model_instance
            entities.append({'eid': eid, 'type': model})

        return entities

    def step(self, time, inputs, max_advance):
        self.time = time
        
        for eid, model_instance in self.entities.items():
            model_instance.step.remote(time_elapsed=time)

        return time + 1

    def get_data(self, outputs):
        data = {}
        for eid, attrs in outputs.items():
            actor = self.entities[eid]
            model = ray.get(actor.get_traffic_lights.remote())
            print(actor)
            print(model)

            data['time'] = self.time
            data[eid] = {}
            for attr in attrs:
                if attr not in self.meta['models']['IntersectionModel']['attrs']:
                    raise ValueError('Unknown output attribute: %s' % attr)
                data[eid][attr] = model
        return data


def main():
    return mosaik_api_v3.start_simulation(IntersectionSim())


if __name__ == '__main__':
    main()