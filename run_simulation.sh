#!/bin/bash

# Check if road_state.txt exists and delete it
if [ -f "data/road_step_history.txt" ]; then
    rm "data/road_step_history.txt"
fi

# Run the Python simulation script with the number of intersections as a command line argument
python3 scenario.py $1
