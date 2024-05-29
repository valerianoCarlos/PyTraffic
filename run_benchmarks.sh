#!/bin/bash

# modes = ("no_scaling" "multithreading" "multithreading_nogil" "multiprocessing" "ray")

mode="ray"
intersections=(5 10)

for n in "${intersections[@]}"; do
    ./run_simulation.sh $n $mode
done

python3 generate_plots.py $mode
