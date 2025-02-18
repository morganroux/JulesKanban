import numpy as np


class StatisticsLogger:
    def __init__(self):
        self.data = []

    def log(self, data):
        self.data.append(data)
        # print("--------stats")
        # print(data)
        # print("------")

    def report(self):
        print("======= REPORT =======")
        unique_tasks = list(set(np.concatenate([d["tasks"] for d in self.data])))
        # for task in unique_tasks:
        #     print(task)
        print(f"number of tasks : {len(unique_tasks)}")
        times = map(
            lambda task: task.finished_at - task.created_at,
            filter(lambda t: t.finished_at is not None, unique_tasks),
        )
        print(f"average time : {np.mean(list(times))}")
