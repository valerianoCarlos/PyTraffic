# PyTraffic

A Python simulation model of a traffic intersection implemented with the Mosaik 3.0 framework.

## How to run

```sh
$ python3 scenario.py
```

## Entities

- **Intersection**: Represents a single intersection managing traffic lights for four cardinal points (north, south, east, west). Alternates between 'red' and 'green' every 10 seconds.
- **Road**: Holds a queue of vehicles moving towards one of the four cardinal points. Can connect to at least one and up to two intersections. Requires information about the destination intersection's traffic light to allow vehicles to pass.
- **Vehicle**: Reads a list of directions (e.g., 'right', 'left', 'straight') and moves accordingly. Determines whether to proceed through the intersection based on the current direction and the state of the traffic light.

### Connections

- Intersection → Vehicle: Sends the state of the traffic light to the Vehicle simulator.
- Road → Intersection: Road simulators need to be connected to one or two intersections to receive information about the state of the traffic light.
- Vehicle → Road: Vehicles are added to specific Road queues upon initialization.

### Inputs and Outputs

- **Intersection**: Inputs: None. Outputs: State of each traffic light.
- **Road**: Inputs: State of the traffic light at the connected intersection(s). Outputs: None.
- **Vehicle**: Inputs: List of directions, state of the traffic light at the intersection it's approaching. Outputs: None.

## Behavior

- Intersection alternates traffic lights between 'red' and 'green' every 10 seconds.
- Vehicles wait in Road queues until the traffic light at the intersection is green in their intended direction.
- Vehicles proceed through the intersection when the traffic light is green, according to their intended direction.
