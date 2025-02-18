import numpy as np


class StatisticsLogger:
    def __init__(self, _settings):
        self.data = []
        self.settings = _settings

    def log(self, data):
        self.data.append(data)
        # print("--------stats")
        # print(data)
        # print("------")

    def build_report(self):
        unique_tasks = list(set(np.concatenate([d["tasks"] for d in self.data])))
        # for task in unique_tasks:
        #     print(task)
        times = list(
            map(
                lambda task: task.finished_at - task.created_at,
                filter(lambda t: t.finished_at is not None, unique_tasks),
            )
        )
        n_workers = sum(self.settings["workers"].values())
        return {
            "tasks": len(unique_tasks),
            "average_time": np.mean(times),
            "workers": n_workers,
        }
