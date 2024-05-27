#!/bin/bash

# modes=("master" "feature/multithreading" "feature/multiprocessing" "feature/ray")
modes=("feature/multithreading")
intersections=(5 10 50)

for mode in "${modes[@]}"; do
    git checkout $mode
    for n in "${intersections[@]}"; do
        ./run_simulation.sh $n $mode
    done
done