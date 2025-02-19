from collections import deque
import time


colors = [
    "\033[91m",
    "\033[92m",
    "\033[93m",
    "\033[94m",
    "\033[95m",
    "\033[96m",
    "\033[97m",
    "\033[98m",
    "\033[99m",
    "\033[100m",
    "\033[101m",
    "\033[102m",
    "\033[103m",
    "\033[104m",
    "\033[105m",
    "\033[106m",
    "\033[107m",
    "\033[108m",
    "\033[109m",
    "\033[110m",
    "\033[111m",
    "\033[112m",
    "\033[113m",
    "\033[114m",
    "\033[115m",
    "\033[116m",
    "\033[117m",
    "\033[118m",
    "\033[119m",
    "\033[120m",
    "\033[121m",
    "\033[122m",
]


verbose = False


def color_print(message, obj):
    if not verbose:
        return
    color = colors[hash(obj) % len(colors)]
    reset_color = "\033[0m"
    print(f"{color}{message}{reset_color} - {hex(id(obj))}")


class IProduct:
    pass


class IStation:
    def __init__(self, sources=None):
        self.sources: list[IStation] = sources if sources else []
        self.todos: deque[IProduct] = deque()
        self.dones: deque[IProduct] = deque()
        self.callers: deque[IStation] = deque()

    def work(self):
        raise NotImplementedError

    def pull(self, caller=None):
        raise NotImplementedError

    def push(self, element):
        raise NotImplementedError


class StationFifo(IStation):

    def can_work(self):
        return True

    def work(self):
        color_print("Working", self)
        if self.todos:
            element = self.todos.popleft()
            self.done(element)

    def done(self, element):
        color_print(f"Done: {element}", self)
        if self.callers:
            caller = self.callers.popleft()
            caller.push(element)
        else:
            self.dones.append(element)

    def push(self, element):
        color_print(f"Pushing: {element}", self)
        self.todos.append(element)
        if self.can_work():
            self.work()

    def pull(self, caller=None):
        color_print("Pulling", self)
        if self.dones:
            element = self.dones.popleft()
            if caller:
                caller.push(element)
            return
        if caller:
            self.callers.append(caller)
        for station in self.sources:
            station.pull(self)


class StationPrinter(StationFifo):
    def work(self):
        if len(self.todos) == 2:
            print(f"PRINT THIS: {self.todos[0], self.todos[1]}")
            self.todos.clear()


if __name__ == "__main__":
    station1 = StationFifo()
    station2 = StationFifo()
    printer = StationPrinter([station1, station2])

    color_print("station1", station1)
    color_print("station2", station2)
    color_print("printer", printer)

    print("======= Test ========")
    time.sleep(2)
    print("-> Pushing A and B at start")
    station1.push("A")
    station2.push("B")
    time.sleep(2)
    print("-> Pulling from printer")
    printer.pull()
    time.sleep(2)
    print("-> Pulling from printer")
    printer.pull()
    time.sleep(2)
    print("-> Pushing C at start")
    station1.push("C")
    time.sleep(2)
    print("-> Pushing D at start")
    station2.push("D")
