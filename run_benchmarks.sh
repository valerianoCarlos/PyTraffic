#!/bin/bash

# modes=("master" "feature/multithreading" "feature/multiprocessing" "feature/ray")
modes=("master")
intersections=(5 10 25)

for mode in "${modes[@]}"; do
    git checkout $mode
    for n in "${intersections[@]}"; do
        ./run_simulation.sh $n $mode
    done
done