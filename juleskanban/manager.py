class TaskManager:
    def __init__(
        self,
        _task_generator,
        _worker_pool,
        _statistics_logger,
        _clock,
        _settings,
    ):
        self.task_generator = _task_generator
        self.worker_pool = _worker_pool
        self.clock = _clock
        self.stats = _statistics_logger
        self.tasks = []
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
        self.tasks += self.task_generator.generate(self.tasks)
        self.assign_empty_tasks()
        self.worker_pool.make_work()
        self.clock.step()

    def start(self):
        self.stats.log(self.__dict__)
        while not self.clock.is_over():
            self.step()
            self.stats.log(self.__dict__)
            if self.interactive:
                input()
