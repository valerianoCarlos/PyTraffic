#!/bin/bash

# Check if road_state.txt exists and delete it
if [ -f "data/road_step_history.txt" ]; then
    rm "data/road_step_history.txt"
fi

# Run the Python simulation script with the number of intersections as a command line argument
# python3.13t -Xgil=0 scenario.py $1 $2   # command for running no gil interpreter with python3.13t
python3 scenario.py $1 $2
