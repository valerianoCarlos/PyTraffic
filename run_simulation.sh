#!/bin/bash

# Check if road_state.txt exists and delete it
if [ -f "data/road_state.txt" ]; then
    rm "data/road_state.txt"
fi

# Run the Python simulation script with the number of intersections as a command line argument
python3 scenario.py $1
