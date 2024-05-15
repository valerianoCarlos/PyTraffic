import json
import sys

"""

Work in progress. Script to convert the road_step_history.txt file to a json file.
"""

def parse_vehicle(vehicle_info):
    # TODO: parse the vehicle info
    vehicle = {}
    return vehicle

def convert_to_json(input_file, output_file):
    data = {}
    current_step = None
    current_road = None
    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('Step'):
                step_id = line.strip(':')
                data[step_id] = []
                current_step = step_id
            elif line.startswith('Road'):
                road_id = line.strip(':')
                current_road = road_id
                data[current_step].append({road_id: {}})
            elif line.startswith('Vehicle'):
                vehicle_id, vehicle_info = line.split(':')
                vehicle = parse_vehicle(vehicle_info)
                data[current_step][-1][current_road]['vehicles_queue'].append({vehicle_id: vehicle})
            else:
                road = data[current_step][-1][current_road]
                if line.startswith('dir'):
                    road['dir'] = line.split('=')[1]
                elif line.startswith('num_vehicles'):
                    road['num_vehicles'] = line.split('=')[1]
                elif line.startswith('vehicles_queue'):
                    road['vehicles_queue'] = []
                elif line.startswith('adjacent_roads'):
                    road['adjacent_roads'] = []
                    adj_roads = line.split('=')[1]
                    road['adjacent_roads'] = adj_roads[1:-1].split(', ')

    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_to_json.py input_file output_file")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    convert_to_json(input_file, output_file)
