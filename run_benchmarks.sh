#!/bin/bash

# modes = ("no_scaling" "no_scaling_nogil" "multithreading" "multithreading_nogil" "multiprocessing" "ray")

mode="no_scaling"
intersections=(5 10 25 50)

for n in "${intersections[@]}"; do
    ./run_simulation.sh $n $mode
done

# python3 utility/generate_plots.py $mode
