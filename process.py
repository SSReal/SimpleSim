from environment import Environment, Event
import random

class ProcessCreationEvent(Event):
    def __init__(self, env: Environment, proc, req_time = None):
        if(req_time is None):
            super().__init__(env.curr_time(), [proc.step])
        else:
            super().__init__(req_time, [proc.step])

class Process:
    def __init__(self, env:Environment, req_time=None):
        self._env = env
        self._generator = self.run()
        self._env.add_event(ProcessCreationEvent(self._env, self, req_time))
    
    def run(self):
        raise NotImplementedError(self)
    
    def step(self):
        return next(self._generator)
    
    

if __name__ == "__main__":
    #testing
    env = Environment(real_time = True)
    class TestProcess(Process):
        def __init__(self, env:Environment):
            super().__init__(env)
        
        def run(self):
            come_time = random.uniform(0, 4)
            wait_time = random.uniform(0, 10)
            serve_time = random.uniform(0, 5)
            go_time = random.uniform(0,4)
            print(f"person id {id(self)} will come in {come_time}, \n\tthen wait for {wait_time}, \n\tthen be served for {serve_time}, \n\tand finally go away in {go_time}")
            self._env.add_event(Event(trigger_time = self._env.curr_time() + come_time, callbacks = [self.step]))
            yield
            print(f"person id {id(self)} done coming, now they will wait")
            self._env.add_event(Event(trigger_time = self._env.curr_time() + wait_time, callbacks = [self.step]))
            yield
            print(f"person id {id(self)} done waiting, now they will be served")
            self._env.add_event(Event(trigger_time = self._env.curr_time() + serve_time, callbacks = [self.step]))
            yield
            print(f"person id {id(self)} done serving, now they will go")
            self._env.add_event(Event(trigger_time = self._env.curr_time() + go_time, callbacks = [self.step]))
            yield
            print(f"person id {id(self)} done with everything")
            return 
    
    t = TestProcess(env)
    env.run()
