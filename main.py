from task import SimpleTaskGenerator
from worker import WorkerPool
from displayer import Displayer
from commons import WORK_TYPE
from statisticsLogger import StatisticsLogger


class TaskManager:
    def __init__(
        self, _task_generator, _worker_pool, _displayer, _statistics_logger, _settings
    ):
        self.task_generator = _task_generator
        self.worker_pool = _worker_pool
        self.displayer = _displayer
        self.stats = _statistics_logger
        self.tasks = []
        self.steps = 0
        self.max_steps = _settings["max_steps"]
        self.interactive = _settings["interactive"]
        self.verbose = _settings["verbose"]

    def assign_empty_tasks(self):
        for task in [t for t in self.tasks if not t.busy() and not t.done()]:
            try:
                worker = self.worker_pool.find_free_worker(task)
                worker.start_task(task)
                task.assign(worker)
            except Exception as e:
                print(e)
                print(f"No worker available for task {task.name}")

    def step(self):
        self.tasks += self.task_generator.generate(self.tasks, self.steps)
        self.assign_empty_tasks()
        self.worker_pool.make_work()
        self.steps += 1

    def start(self):
        self.displayer.print(self.__dict__)
        self.stats.log(self.__dict__)
        while self.steps < self.max_steps:
            self.step()
            if self.verbose:
                self.displayer.print(self.__dict__)
            self.stats.log(self.__dict__)
            if self.interactive:
                input()


settings = {
    "workers": {WORK_TYPE[0]: 1, WORK_TYPE[1]: 2, WORK_TYPE[2]: 1},
    "work_sizes": {
        WORK_TYPE[0]: 10,
        WORK_TYPE[1]: 30,
        WORK_TYPE[2]: 20,
    },
    "interactive": False,
    "verbose": True,
    "max_steps": 15,
}

if __name__ == "__main__":
    worker_pool = WorkerPool(settings["workers"])
    displayer = Displayer()
    statistics_logger = StatisticsLogger()
    task_generator = SimpleTaskGenerator(settings["work_sizes"])
    task_manager = TaskManager(
        task_generator, worker_pool, displayer, statistics_logger, settings
    )
    task_manager.start()
    statistics_logger.report()
