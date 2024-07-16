from concurrent.futures import ThreadPoolExecutor
import json
import collections
import mosaik_api_v3

META = {
    "type": "event-based",
    "models": {
        "Monitor": {
            "public": True,
            "any_inputs": True,
            "params": [],
            "attrs": [],
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
            raise RuntimeError("Can only create one instance of Monitor.")

        self.eid = "Monitor"
        return [{"eid": self.eid, "type": model}]

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
        output_file = "data/collected_data.json"
        
        def prepare_data_chunk(data_chunk):
            chunk_data = {}
            for src, attrs in data_chunk:
                chunk_data[src] = attrs
            return chunk_data

        data_items = list(self.data.items())
        chunk_size = max(len(data_items) // 4, 1)

        with ThreadPoolExecutor() as executor:
            chunks = [data_items[i:i + chunk_size] for i in range(0, len(data_items), chunk_size)]
            results = list(executor.map(prepare_data_chunk, chunks))

        combined_data = {}
        for chunk in results:
            combined_data.update(chunk)

        with open(output_file, "w") as f:
            json.dump(combined_data, f, indent=4)

        print(f"Collected data written to {output_file}")


if __name__ == "__main__":
    mosaik_api_v3.start_simulation(Collector())
