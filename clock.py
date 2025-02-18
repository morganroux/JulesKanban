class Clock:
    def __init__(self, _max_steps=10):
        self.steps = 0
        self.max_steps = _max_steps

    def get_current(self):
        return self.steps

    def step(self, inc=1):
        self.steps += inc

    def is_over(self):
        return self.steps > self.max_steps
