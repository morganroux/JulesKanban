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
        n_tasks = np.unique(
            np.concatenate([[t.name for t in d["tasks"]] for d in self.data])
        )
        print(f"number of tasks : {len(n_tasks)}")
