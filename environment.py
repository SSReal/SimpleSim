import time
from heapq import heappush, heappop
import random


class InvalidEventError(Exception):
    pass


class EmptySchedule(Exception):
    pass


class Event:

    def __init__(self, trigger_time: float, callbacks=[]):
        # print(f"\n---event created with trigger {trigger_time:2.2f}---\n")
        self.trigger_time = trigger_time
        self.callbacks = callbacks

    def process(self, currTime):
        # print(
        #     f"\n---event start at {self.trigger_time:2.2f}; environment time: {currTime:2.2f}---\n"
        # )
        for f in self.callbacks:
            try:
                f()
            except StopIteration:
                continue

    def getTime(self):
        return self.trigger_time

    def __lt__(self, other):
        return self.trigger_time < other.trigger_time


class Environment:

    def __init__(self,
                 st_time=0,
                 en_time=100,
                 factor=1,
                 is_real_time=False,
                 force=False):
        self.start_time = st_time
        self.end_time = en_time
        self.factor = factor
        self._queue = []
        self._time = self.start_time
        self.is_real_time = is_real_time
        self.force = force

    def run(self):
        while self._time <= self.end_time:
            try:
                self.step()
            except EmptySchedule:
                # print("finished")
                return

    def step(self):
        # wait till enough time passes in the real world, if real time
        self.wait()
        while self.force or (len(self._queue) > 0
                             and self.next_event_time() <= self._time):
            curr_event = heappop(self._queue)
            try:
                curr_event.process(self._time)
            except:
                raise InvalidEventError()

    def wait(self):
        w_en_time = self.next_event_time()
        if (self.is_real_time):
            w_st_time = self._time
            real_st_time = time.perf_counter()
            curr_time = time.perf_counter()
            real_time = real_st_time + (w_en_time - w_st_time) * self.factor
            while True:
                delta = real_time - curr_time
                if (delta <= 0): break
                time.sleep(delta)
                curr_time = time.perf_counter()
        self._time = w_en_time

    def next_event_time(self):
        if (len(self._queue) == 0):
            raise EmptySchedule()
        else:
            return self._queue[0].getTime()

    def add_event(self, event):
        heappush(self._queue, event)

    def curr_time(self):
        return self._time


if __name__ == "__main__":
    env = Environment(factor=0.5, is_real_time=True)
    for i in range(0, 50):
        env.add_event(Event(random.uniform(0, 20)))

    env.run()
