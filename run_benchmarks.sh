#!/bin/bash

# modes = ("no_scaling" "multithreading" "multithreading_nogil" "multiprocessing" "ray")

mode="multithreading"
intersections=(5 10 25 50)

for n in "${intersections[@]}"; do
    ./run_simulation.sh $n $mode
done

# python3 generate_plots.py $mode
