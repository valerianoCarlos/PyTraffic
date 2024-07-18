from concurrent.futures import ThreadPoolExecutor, as_completed
import collections
import json
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
        self.output_file = "data/collected_data.json"

    def init(self, sid, time_resolution):
        return self.meta

    def create(self, num, model):
        if num > 1 or self.eid is not None:
            raise RuntimeError("Can only create one instance of Monitor.")

        self.eid = "Monitor"
        return [{"eid": self.eid, "type": model}]

    def step(self, time, inputs, max_advance):
        data = inputs.get(self.eid, {})
        for attr, values in data.items():
            for src, value in values.items():
                self.data[src][attr][time] = value

        return None

    def finalize(self):
        num_threads = 10
        data_chunks = self.split_data(self.data, num_threads)
        
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(json.dumps, chunk, indent=4) for chunk in data_chunks]
            serialized_chunks = [future.result() for future in as_completed(futures)]
        
        with open(self.output_file, "w") as f:
            for chunk in serialized_chunks:
                f.write(chunk)
        
        print(f"Collected data written to {self.output_file}")

    def split_data(self, data, num_chunks):
        items = list(data.items())
        chunk_size = max(1, len(items) // num_chunks)
        return [dict(items[i * chunk_size:(i + 1) * chunk_size]) for i in range(num_chunks)]

if __name__ == "__main__":
    mosaik_api_v3.start_simulation(Collector())
