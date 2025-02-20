class Clock:
    def __init__(self, _max_steps=10, inc=1):
        self.steps = 0
        self.max_steps = _max_steps
        self.inc = inc

    def get_current(self):
        return self.steps

    def get_inc(self):
        return self.inc

    def reset(self):
        self.steps = 0

    def step(self):
        self.steps += self.inc

    def is_over(self):
        return self.steps > self.max_steps
