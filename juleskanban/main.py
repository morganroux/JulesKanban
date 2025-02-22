from .manager import TaskManager
from .optimizer import Optimizer, EfficiencyOptimizer
from .commons import WORK_TYPE
from .clock import Clock
from .task import SimpleTaskGenerator
from .worker import WorkerPool
from .displayer import withDisplay
from .statisticsLogger import StatisticsLogger


if __name__ == "__main__":

    settings = {
        "workers": {WORK_TYPE[0]: 1, WORK_TYPE[1]: 2, WORK_TYPE[2]: 2},
        "work_sizes": {
            WORK_TYPE[0]: 10,
            WORK_TYPE[1]: 30,
            WORK_TYPE[2]: 20,
        },
        "interactive": False,
        "verbose": True,
        "max_steps": 100,
    }

    clock = Clock(settings["max_steps"])
    worker_pool = WorkerPool(settings["workers"])
    statistics_logger = StatisticsLogger(settings)
    task_generator = SimpleTaskGenerator(clock, settings["work_sizes"])
    task_manager = withDisplay(
        TaskManager(task_generator, worker_pool, statistics_logger, clock, settings)
    )
    task_manager.start()

    print(statistics_logger.build_report())

    # settings = {
    #     "workers": {WORK_TYPE[0]: 1, WORK_TYPE[1]: 1, WORK_TYPE[2]: 2},
    #     "work_sizes": {WORK_TYPE[0]: 10, WORK_TYPE[1]: 30, WORK_TYPE[2]: 20},
    #     "interactive": False,
    #     "verbose": False,
    #     "max_steps": 100,
    # }

    # optimizer = EfficiencyOptimizer(settings)
    # optimal_workers = optimizer.optimize_workers()
    # print(f"Optimal Worker Allocation: {optimal_workers}")
