from environment import Environment, Event
from process import Process
import random

class Resource:
    def __init__(self, env: Environment, capacity: int):
        self._env = env
        self._queue = []
        self.available = capacity
        self._generator = self.run()
        self._env.add_event(Event(self._env.curr_time(), callbacks=[self.step]))
    
    def step(self):
        return next(self._generator)
    
    def run(self):
        while True:
            while(self.available == 0): 
                # no resource units to allocate
                yield
            while(len(self._queue) == 0):
                # no one waiting
                yield
            # someone is waiting
            self.available -= 1
            # print(self.available)
            usr = self._queue.pop(0)
            usr()

    def request(self, usr):
        self._queue.append(usr)
        self._env.add_event(Event(self._env.curr_time(), [self.step]))

    def release(self):
        self.available += 1
        self._env.add_event(Event(self._env.curr_time(), [self.step]))
    
if __name__ == "__main__":
    class TestProcess(Process):
        def __init__(self, env, res:Resource, req_time=None):
            super().__init__(env, req_time)
            self.res = res # the resource to request

        def run(self):
            print(f"process created with id {id(self)}")
            print("requesting the resource")
            yield res.request(self.step)
            #got the resource
            print(f"process {id(self)} got the resource")
            print("holding the resource")
            yield self._env.add_event(Event(self._env.curr_time() + 2, [self.step]))
            #held the resource
            print(f"process {id(self)} done with the resource")
            print("releasing the resource")
            self.res.release()

    env = Environment(real_time = True)
    res = Resource(env, 3)
    ts = [TestProcess(env, res, random.randint(0,3)) for i in range(0, 5)]
    env.run()




