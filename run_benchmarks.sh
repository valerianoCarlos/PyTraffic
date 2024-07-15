#!/bin/bash

mode="heavy_no_scaling"
intersections=(5 10 25 50)

for n in "${intersections[@]}"; do
    ./run_simulation.sh $n $mode
done

# python3 utility/generate_plots.py $mode
