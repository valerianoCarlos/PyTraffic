import mosaik_api_v3
import models.road_model as road_model

META = {
    'type': 'event-based',
    'models': {
        'RoadModel': {
            'public': True,
            'params': ['from_direction'],
            'attrs': ['traffic_lights_in'],
        },
    },
}


class RoadSim(mosaik_api_v3.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid_prefix = 'Road_'
        self.road_entities = {}
        self.time = 0

    def create(self, num, model, from_direction):
        n_roads = len(self.road_entities)
        entities = []
        for i in range(n_roads, n_roads + num):
            model_instance = road_model.RoadModel(from_direction)
            eid = '%s%d' % (self.eid_prefix, i)
            self.road_entities[eid] = model_instance
            entities.append({'eid': eid, 'type': model})

        return entities

    def step(self, time, inputs, max_advance):
        self.time = time
        data = {}
        for eid, attrs in inputs.items():
            tl_dict = attrs.get('traffic_lights_in', {})
            if len(tl_dict) != 1:
                raise RuntimeError('Only one ingoing connection allowed per road, but "%s" has %i.' % (eid, len(tl_dict)))
            tl = list(tl_dict.values())[0]
            
            self.road_entities[eid].step(tl)
            
            data[eid] = {'traffic_lights_in': tl}
        
        self.data = data
        return None
            
    def get_data(self, outputs):
        data = {}
        for eid, attrs in outputs.items():
            for attr in attrs:
                if attr != 'traffic_lights_in':
                    raise ValueError('Unknown output attribute "%s"' % attr)
                if eid in self.data:
                    data['time'] = self.time
                    data.setdefault(eid, {})[attr] = self.data[eid][attr]

        return data
