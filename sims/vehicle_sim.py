import mosaik_api_v3
import models.vehicle_model as vehicle_model

META = {
    'type': 'event-based',
    'models': {
        'VehicleModel': {
            'public': True,
            'params': ['init_road', 'id'],
            'attrs': ['curr_road', 'curr_state'],
        },
    },
}


class VehicleSim(mosaik_api_v3.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid_prefix = 'Vehicle_'
        self.vehicle_entities = {}
        self.time = 0

    def create(self, num, model, init_road):
        n_roads = len(self.vehicle_entities)
        entities = []
        for i in range(n_roads, n_roads + num):
            model_instance = vehicle_model.VehicleModel(init_road, i)
            print(model_instance)
            eid = '%s%d' % (self.eid_prefix, i)
            self.vehicle_entities[eid] = model_instance
            entities.append({'eid': eid, 'type': model})
        return entities

    def step(self, time, inputs, max_advance):
        self.time = time
        data = {}
        for eid, attrs in inputs.items():
            vehicle_state = attrs.get('next_state', {})
            if len(vehicle_state) != 1:
                raise RuntimeError('Only one ingoing connection allowed per road, but "%s" has %i.' % (eid, len(vehicle_state)))
            next_state = list(vehicle_state.values())[0]
            
            self.vehicle_entities[eid].step(next_state)
            
            data[eid] = {'next_state': next_state}
        
        self.data = data
        return None
            
    def get_data(self, outputs):
        data = {}
        for eid, attrs in outputs.items():
            for attr in attrs:
                if attr != 'next_state':
                    raise ValueError('Unknown output attribute "%s"' % attr)
                if eid in self.data:
                    data['time'] = self.time
                    data.setdefault(eid, {})[attr] = self.data[eid][attr]

        return data
