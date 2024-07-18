#!/bin/bash

# modes_low = ("no_scaling" "multithreading" "multithreading_nogil" "multiprocessing" "ray")
# modes_high = ("no_scaling_high" "multithreading_high" "multithreading_nogil_high" "multiprocessing_high" "ray_high")

mode="ray_high"
intersections=(5 10 25 50)

for n in "${intersections[@]}"; do
    ./run_simulation.sh $n $mode
done

# python3 utility/generate_plots.py $mode
