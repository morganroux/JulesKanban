from collections import deque
import time

from juleskanban.clock import Clock


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


class SimpleProduct(IProduct):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"({self.name})"

    def __repr__(self):
        return self.__str__()


class CookedProduct(SimpleProduct):
    def __init__(self, product: SimpleProduct):
        super().__init__(product.name)
        self.name = product.name + "_cooked"


class IStation:
    def __init__(
        self, clock: Clock, sources: list["IStation"], destinations: list["IStation"]
    ):
        self.sources: list[IStation] = sources
        self.destinations: list[IStation] = destinations
        self.clock = clock
        self.todos: deque[IProduct] = deque()
        self.dones: deque[IProduct] = deque()
        self.pullers: deque[IStation] = deque()

    def work(self):
        raise NotImplementedError

    def pull(self, puller=None):
        raise NotImplementedError

    def push(self, element):
        raise NotImplementedError

    def step(self):
        pass

    def add_source(self, source):
        self.sources.append(source)

    def add_destination(self, destination):
        self.destinations.append(destination)


class StationFifo(IStation):

    def work(self):
        raise NotImplementedError

    def done(self, element):
        color_print(f"Done: {element}", self)
        try:
            if self.destinations:
                self.destinations[0].push(element)
                return
        except Exception as e:
            print(e)
        self.dones.append(element)
        self.push_to_pullers()

    def push_to_pullers(self):
        while self.pullers and self.dones:
            puller = self.pullers.popleft()
            element = self.dones.popleft()
            puller.push(element)

    def push(self, element):
        color_print(f"Pushing: {element}", self)
        self.todos.append(element)
        self.work()

    def pull(self, puller=None):
        color_print("Pulling", self)
        if not puller:
            self.forward_pull()
            return
        self.pullers.append(puller)
        self.push_to_pullers()
        if self.pullers:
            self.forward_pull()

    def forward_pull(self):
        raise NotImplementedError


class StationFifoBasic(StationFifo):
    def work(self):
        color_print("Working", self)
        if self.todos:
            element = self.todos.popleft()
            self.done(element)

    def forward_pull(self):
        for station in self.sources:
            station.pull(self)


class StationFifoCooker(StationFifo):

    def __init__(self, clock, sources: list[StationFifo]):
        super().__init__(clock, sources, [])
        self.elasped_time = 0
        self.cooking_time = 10
        self.cookings: list[IProduct] = []
        self.capacity = 3

    def work(self):
        while self.todos and len(self.cookings) < 3:
            self.cookings.append(self.todos.popleft())
        if len(self.cookings) == self.capacity:
            print("Cooking", self)
            self.elasped_time += self.clock.get_inc()
            if self.elasped_time >= self.cooking_time:
                self.done(CookedProduct(self.cookings[0]))
                # delete objects ?
                self.cookings.clear()
                self.elasped_time = 0

    def step(self):
        self.work()

    def forward_pull(self):
        i = 0
        products_needed = len(self.pullers) - len(self.cookings) - len(self.todos)
        if products_needed <= 0:
            return
        batchsNeeded = int(products_needed / 3) + 1
        products_to_pull = batchsNeeded * 3
        while products_to_pull > i:
            for station in self.sources:
                print("===pull station")
                station.pull(self)
            i += 1


class StationFifoPrinter(StationFifo):
    def work(self):
        if len(self.todos) == 2:
            print(f"PRINT THIS: {self.todos[0], self.todos[1]}")
            self.todos.clear()

    def forward_pull(self):
        for station in self.sources:
            station.pull(self)


def simple_test():
    clock = Clock(100)
    station1 = StationFifoBasic(clock, [], [])
    station2 = StationFifoBasic(clock, [], [])
    printer = StationFifoPrinter(clock, [station1, station2], [])

    color_print("station1", station1)
    color_print("station2", station2)
    color_print("printer", printer)

    print("======= Test ========")
    time.sleep(2)
    print("-> Pushing A and B at start")
    station1.push(SimpleProduct("A1"))
    station2.push(SimpleProduct("B"))
    time.sleep(2)
    print("-> Pulling from printer")
    printer.pull()
    printer.pull()
    time.sleep(2)
    print("-> Pushing C at start")
    station1.push(SimpleProduct("C1"))
    time.sleep(2)
    station2.push(SimpleProduct("D"))


def test_cooking():
    clock = Clock(100)
    station1 = StationFifoBasic(clock, [], [])
    cooker = StationFifoCooker(clock, [station1])

    # if pulling : comment this. If pushing, uncomment this
    station1.add_destination(cooker)
    ##
    station2 = StationFifoBasic(clock, [], [])
    printer = StationFifoPrinter(clock, [cooker, station2], [])

    stations = [station1, cooker, station2, printer]

    color_print("station1", station1)
    color_print("station2", station2)
    color_print("cooker", cooker)
    color_print("printer", printer)

    print("======= Test ========")
    time.sleep(2)
    print("-> Pushing A and B at start")
    station1.push(SimpleProduct("A1"))
    station1.push(SimpleProduct("A2"))
    station1.push(SimpleProduct("A3"))
    station2.push(SimpleProduct("B"))
    print("-> Pulling from printer")
    printer.pull()
    while clock.get_current() < 15:
        print(f"Step {clock.get_current()}")
        for station in stations:
            station.step()
        clock.step()
        time.sleep(1)

    time.sleep(2)

    print("-> Pushing C at start")
    station1.push(SimpleProduct("C1"))
    station1.push(SimpleProduct("C2"))
    station1.push(SimpleProduct("C3"))
    station2.push(SimpleProduct("D"))
    while clock.get_current() < 40:
        print(f"Step {clock.get_current()}")
        for station in stations:
            station.step()
        clock.step()
        time.sleep(1)
        if clock.get_current() == 20:
            print("-> Pulling from printer")
            printer.pull()


def main():
    # simple_test()
    test_cooking()


if __name__ == "__main__":
    main()
