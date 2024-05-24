"""
A simple data collector that prints all data when the simulation finishes.

"""
import collections
import json
import mosaik_api_v3
from concurrent.futures import ThreadPoolExecutor

META = {
    'type': 'event-based',
    'models': {
        'Monitor': {
            'public': True,
            'any_inputs': True,
            'params': [],
            'attrs': [],
        },
    },
}


class Collector(mosaik_api_v3.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid = None
        self.data = collections.defaultdict(lambda: collections.defaultdict(dict))

    def init(self, sid, time_resolution):
        return self.meta

    def create(self, num, model):
        if num > 1 or self.eid is not None:
            raise RuntimeError('Can only create one instance of Monitor.')

        self.eid = 'Monitor'
        return [{'eid': self.eid, 'type': model}]

    def step(self, time, inputs, max_advance):
        data = inputs.get(self.eid, {})
        
        def process_input(attr, values):
            for src, value in values.items():
                self.data[src][attr][time] = value

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_input, attr, values) for attr, values in data.items()]
            for future in futures:
                future.result()

        return None

    def finalize(self):
        output_file = 'data/collected_data.json'
        with open(output_file, 'w') as f:
            json.dump(self.data, f, indent=4)
        print(f'Collected data written to {output_file}')


if __name__ == '__main__':
    mosaik_api_v3.start_simulation(Collector())
