import mosaik_api_v3
import models.road_model as road_model
import json

META = {
    'type': 'event-based',
    'models': {
        'RoadModel': {
            'public': True,
            'params': ['from_direction', 'num_vehicles', 'next_adjacent_roads'],
            'attrs': ['traffic_lights_in', 'num_vehicles'],
        },
    },
    'extra_methods': [
        'initialize_road_adjacencies',
        'print_road_state',
    ],
}


class RoadSim(mosaik_api_v3.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid_prefix = 'Road_'
        self.road_entities = {}
        self.vehicles_count = 0
        self.time = 0
        
    def initialize_road_adjacencies(self, adjacency_map):
        for eid, adjacencies in adjacency_map.items():
            road_model_instance = self.road_entities[eid]
            updated_adjacencies = []
            for adjacency in adjacencies:
                road_instance = self.road_entities[adjacency['road']]   # get the RoadModel entity for the eid of the road
                updated_adjacencies.append({'road': road_instance, 'direction': adjacency['direction']})
            road_model_instance.next_adjacent_roads = updated_adjacencies
        self.print_road_state()

    def create(self, num, model, from_direction, num_vehicles):
        n_roads = len(self.road_entities)
        entities = []
        for i in range(n_roads, n_roads + num):
            eid = '%s%d' % (self.eid_prefix, i)
            model_instance = road_model.RoadModel(eid, from_direction, num_vehicles, self.vehicles_count)
            self.vehicles_count += num_vehicles
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
        self.print_road_state()
        return None
            
    def get_data(self, outputs):
        data = {}
        for eid, attrs in outputs.items():
            model = self.road_entities[eid]
            data['time'] = self.time
            data[eid] = {}
            for attr in attrs:
                if attr not in self.meta['models']['RoadModel']['attrs']:
                    raise ValueError('Unknown output attribute: %s' % attr)
                
                data[eid][attr] = getattr(model, attr)

        return data
    
    def print_road_state(self):
        with open('data/road_state.txt', 'a') as f:
            for road in self.road_entities.values():
                f.write(str(road))
                f.write('\n\n')
    

def main():
    return mosaik_api_v3.start_simulation(RoadSim())

if __name__ == '__main__':
    main()
