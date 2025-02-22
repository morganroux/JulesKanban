from typing import Any, TypedDict
import numpy as np

from juleskanban.manager import MainSettings
from juleskanban.task import Task


class LogData(TypedDict):
    tasks: list[Task]


class StatisticsLogger:
    def __init__(self, _settings: MainSettings):
        self.data: list[Any] = []
        self.settings = _settings

    def log(self, data: Any):
        self.data.append(data)
        # print("--------stats")
        # print(data)
        # print("------")

    def build_report(self):
        unique_tasks: list[Task] = list(
            set(np.concatenate([d["tasks"] for d in self.data]))  # pyright: ignore
        )
        # for task in unique_tasks:
        #     print(task)
        finished_tasks = list(filter(lambda t: t.finished_at is not None, unique_tasks))
        times: list[int] = list(
            map(
                lambda task: task.finished_at - task.created_at,  # pyright: ignore
                finished_tasks,
            )
        )  # pyright: ignore
        n_workers = sum(self.settings["workers"].values())
        return {
            "tasks": len(unique_tasks),
            "average_time": np.mean(times),
            "workers": n_workers,
        }
