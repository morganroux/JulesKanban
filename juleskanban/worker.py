from juleskanban.commons import WorkType
from juleskanban.task import Task


class Worker:
    def __init__(self, wtype: WorkType, amount: int = 10):
        self.type: WorkType = wtype
        self.amount: int = amount
        self.tasks: list[Task] = []

    def work(self, ratio: int = 100):
        amount = self.amount * ratio / 100
        if not self.tasks:
            return

        amount_per_task = int(amount / len(self.tasks))
        for task in self.tasks:
            task.update_work(self.type, amount_per_task)
            if task.work_completed(self.type):
                self.finish_task(task)

    def start_task(self, task: Task):
        self.tasks.append(task)

    def finish_task(self, task: Task):
        task.finish()
        self.tasks.remove(task)

    def full(self):
        return len(self.tasks) >= 1


class WorkerPool:
    def __init__(self, _workers: dict[WorkType, int]):
        self.workers: list[Worker] = []
        for work_type, size in _workers.items():
            for _ in range(size):
                self.create_worker(work_type)

    def create_worker(self, wtype: WorkType):
        worker = Worker(wtype)
        self.workers.append(worker)
        return worker

    def get_workers(self, wtype: WorkType | None = None):
        if wtype is None:
            return self.workers
        return [op for op in self.workers if op.type == wtype]

    def find_free_worker(self, task: Task):
        state = task.state()

        free_worker = next(
            (op for op in self.workers if op.type == state and not op.full()), None
        )
        if free_worker is None:
            raise Exception(f"No free worker for {state}")

        return free_worker

    def make_work(self, ratio: int = 100):
        for worker in self.workers:
            worker.work(ratio)
