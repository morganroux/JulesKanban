from task import SimpleTaskGenerator
from worker import WorkerPool
from displayer import Displayer
from commons import WORK_TYPE, WORK_SIZES


class TaskManager:
    def __init__(self, task_generator, worker_pool, displayer):
        self.task_generator = task_generator
        self.worker_pool = worker_pool
        self.displayer = displayer
        self.tasks = []

    def init(self, settings):
        for work_type, size in settings["workers"].items():
            for _ in range(size):
                self.worker_pool.create_worker(work_type)
        self.tasks.append(self.task_generator.generate(self.tasks))

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
        self.assign_empty_tasks()
        self.worker_pool.make_work()

    def start(self):
        while True:
            self.displayer.print(self.infos())
            self.step()
            input()

    def infos(self):
        return {"tasks": self.tasks, "workers": self.worker_pool.get_workers()}


settings = {
    "workers": {WORK_TYPE["ANALYSIS"]: 1, WORK_TYPE["DEV"]: 2, WORK_TYPE["QA"]: 1}
}

if __name__ == "__main__":
    worker_pool = WorkerPool()
    displayer = Displayer()
    task_generator = SimpleTaskGenerator(WORK_SIZES)
    task_manager = TaskManager(task_generator, worker_pool, displayer)
    task_manager.init(settings)
    task_manager.start()
