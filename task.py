class Task:
    def __init__(self, name, work_sizes, clock):
        self.name = name
        self.work_left = work_sizes.copy()
        self.operator = None
        self.clock = clock
        self.created_at = self.clock.get_current()
        self.finished_at = None

    def __str__(self):
        return f"Task {self.name} - {self.work_left} - {self.operator}"

    def assign(self, operator):
        self.operator = operator

    def finish(self):
        self.operator = None
        self.finished_at = self.clock.get_current()

    def update_work(self, work_type, work_amount):
        if self.work_left[work_type] == 0:
            raise ValueError(f"{work_type} on this task is already completed")

        self.work_left[work_type] -= work_amount
        if self.work_left[work_type] < 0:
            self.work_left[work_type] = 0

    def work_completed(self, work_type):
        return self.work_left[work_type] == 0

    def busy(self):
        return self.operator is not None

    def state(self):
        for work_type in self.work_left:
            if not self.work_completed(work_type):
                return work_type
        return "DONE"

    def done(self):
        return self.state() == "DONE"


class TaskGenerator:
    def __init__(self, clock, work_sizes):
        self.clock = clock
        self.work_sizes = work_sizes

    def create_task(self, name):
        return Task(name, self.work_sizes, self.clock)

    def generate(self, tasks):
        raise NotImplementedError


class SimpleTaskGenerator(TaskGenerator):
    def __init__(self, clock, work_sizes):
        super().__init__(clock, work_sizes)
        self.id = 0

    def generate(self, tasks):
        if self.clock.get_current() < 3:
            task = self.create_task(f"task-{self.id}")
            self.id += 1
            return [task]
        return []
