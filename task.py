class Task:
    def __init__(self, name, work_sizes):
        self.name = name
        self.work_left = work_sizes.copy()
        self.operator = None

    def __str__(self):
        return f"Task {self.name} - {self.work_left} - {self.operator}"

    def assign(self, operator):
        self.operator = operator

    def unassign(self):
        self.operator = None

    def update_work(self, work_type, work_amount):
        if self.work_left[work_type] == 0:
            raise ValueError(f"{work_type} on this task is already completed")

        self.work_left[work_type] -= work_amount
        if self.work_left[work_type] < 0:
            self.work_left[work_type] = 0

    def work_completed(self, work_type):
        return self.work_left[work_type] == 0

    def fully_completed(self):
        return all(val == 0 for val in self.work_left.values())

    def busy(self):
        return self.operator is not None

    def done(self):
        return self.state() == "DONE"

    def state(self):
        for work_type in self.work_left:
            if not self.work_completed(work_type):
                return work_type
        return "DONE"


class TaskGenerator:
    def __init__(self, work_sizes):
        self.work_sizes = work_sizes

    def create_task(self, name):
        return Task(name, self.work_sizes)

    def generate(self, tasks):
        raise NotImplementedError


class SimpleTaskGenerator(TaskGenerator):
    def __init__(self, work_sizes):
        super().__init__(work_sizes)
        self.id = 0

    def generate(self, tasks):
        task = self.create_task(f"task-{self.id}")
        self.id += 1
        return task
