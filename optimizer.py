import copy
from clock import Clock
from displayer import Displayer
from manager import TaskManager
from statisticsLogger import StatisticsLogger
from task import SimpleTaskGenerator
from worker import WorkerPool


class Optimizer:
    def __init__(self, _settings):
        self.settings = copy.deepcopy(_settings)
        self.task_manager = None
        self.statistics_logger = None

    def reset(self, _settings):
        if _settings:
            self.settings = {**self.settings, **_settings}
        clock = Clock(self.settings["max_steps"])
        worker_pool = WorkerPool(self.settings["workers"])
        displayer = Displayer()
        self.statistics_logger = StatisticsLogger(self.settings)
        task_generator = SimpleTaskGenerator(clock, self.settings["work_sizes"])
        self.task_manager = TaskManager(
            task_generator,
            worker_pool,
            displayer,
            self.statistics_logger,
            clock,
            self.settings,
        )

    def run_simulation(self, settings=None):
        self.reset(settings)
        self.task_manager.start()
        return self.statistics_logger.build_report()


class EfficiencyOptimizer(Optimizer):
    def __init__(self, settings, step_size=1, tolerance=0.01, max_iterations=20):
        super().__init__(settings)
        self.step_size = step_size  # Learning rate for updates
        self.tolerance = tolerance  # Convergence threshold
        self.max_iterations = max_iterations
        self.history = []  # Store worker settings and completion times

    def compute_gradient(self, workers, delta=1):
        result = self.run_simulation({"workers": workers})  # Run with current workers
        base_result = result["average_time"] / result["workers"]  # Base completion time
        gradient = {}

        for work_type in workers.keys():
            test_workers = copy.deepcopy(workers)
            test_workers[work_type] += delta  # Slightly increase workers

            result = self.run_simulation(
                {"workers": test_workers}
            )  # New completion time
            new_result = result["average_time"] / result["workers"]

            # Compute finite difference approximation
            gradient[work_type] = (new_result - base_result) / delta

        return gradient, base_result

    def optimize_workers(self):
        """Optimize worker numbers using gradient descent."""
        workers = copy.deepcopy(self.settings["workers"])

        for i in range(self.max_iterations):
            gradient, base_result = self.compute_gradient(workers)
            self.history.append(
                {"iteration": i, "workers": workers.copy(), "result": base_result}
            )

            # Adjust workers using the negative gradient direction
            for work_type in workers.keys():
                workers[work_type] = int(
                    self.step_size * gradient[work_type]
                )  # Move against gradient

                # Ensure worker count is positive
                workers[work_type] = max(1, workers[work_type])

            print(f"Iteration {i}, Workers: {workers}, Result: {base_result}")

            # Stopping condition: If change in completion time is small
            if (
                i > 0
                and abs(self.history[-1]["result"] - self.history[-2]["result"])
                < self.tolerance
            ):
                print("Converged.")
                break

        return workers
