# Define the scripts
CLEAR_SCRIPT = ./clear_data.sh
PLOTS_SCRIPT = ./plot_data.sh
BENCHMARK_SCRIPT = ./run_benchmarks.sh
SIMULATION_SCRIPT = ./run_simulation.sh

# Define the commands
.PHONY: clear plot test run

# Command to clear data
clear:
	$(CLEAR_SCRIPT)

# Command to plot data
plot:
	$(PLOTS_SCRIPT)

# Command to run benchmarks
test:
	$(BENCHMARK_SCRIPT)

# Command to run simulation
run:
	$(SIMULATION_SCRIPT)
