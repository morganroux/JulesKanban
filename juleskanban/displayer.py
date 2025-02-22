from typing import Any, Callable, cast
from juleskanban.task import Task
from .commons import WORK_TYPE
from .manager import TaskManager


def print_tm(tm: TaskManager):
    data = {
        **tm.__dict__,
        "steps": tm.clock.get_current(),
    }
    tasks = cast(list[Task], data["tasks"])
    print(f"==== Step {data['steps']} =====\n\n")
    print("----Tasks----:\n")
    for work_type in WORK_TYPE:
        print(f"=> {work_type}: ")
        for task in filter(lambda t: t.state() == work_type, tasks):
            print(task)
    print("\n=========\n")


def withDisplay(task_manager: TaskManager):

    def log_func(func: Callable[..., Any]):
        def wrapper(*args: Any, **kwargs: Any):
            print_tm(task_manager)
            return func(*args, **kwargs)

        return wrapper

    task_manager.step = log_func(task_manager.step)
    return task_manager
