import mosaik_api_v3
import models.intersection_model as intersection_model

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
        self.intersection_entities = {}
        self.time = 0

    def init(self, sid, time_resolution):
        if float(time_resolution) != 1.:
            raise ValueError('IntersectionSim only supports time_resolution=1., but %s was set.' % time_resolution)
        return self.meta

    def create(self, num, model):
        next_eid = len(self.intersection_entities)
        entities = []

        for i in range(next_eid, next_eid + num):
            model_instance = intersection_model.IntersectionModel()
            eid = '%s%d' % (self.eid_prefix, i)
            self.intersection_entities[eid] = model_instance
            entities.append({'eid': eid, 'type': model})

        return entities

    def step(self, time, inputs, max_advance):
        self.time = time
        for eid, model_instance in self.intersection_entities.items():
            model_instance.step(time)

        return time + 1

    def get_data(self, outputs):
        data = {}
        for eid, attrs in outputs.items():
            model = self.intersection_entities[eid]
            data['time'] = self.time
            data[eid] = {}
            for attr in attrs:
                if attr not in self.meta['models']['IntersectionModel']['attrs']:
                    raise ValueError('Unknown output attribute: %s' % attr)
                data[eid][attr] = getattr(model, attr)
        return data


def main():
    return mosaik_api_v3.start_simulation(IntersectionSim())


if __name__ == '__main__':
    main()