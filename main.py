'''Simple example, just for the future me, when he will have again doubts about this'''

import time


class Task():
    def __init__(
            self,
            name: str,
            wait: int,
            cb):
        self.name = name
        self.wait = wait
        self.cb = cb
        self.done = False

    def get_corutine(self):
        print(f"Starting task {self.name}")
        t = yield(self.wait)
        
        while(t < self.wait):
            t = yield(self.wait - t)
        
        self.done = True
        return self.cb()

    def is_done(self):
        return self.done


class EventLoop:
    def __init__(self):
        self.tasks = {}
        self.time = 0

    def register_task(self, task: Task):
        # For each task create a coroutine
        self.tasks[task] = task.get_corutine()
        return self
    
    def run(self):
        # "Prime" the coroutines
        for task, cor in self.tasks.items():
            next(cor)
        
        while True:
            # Next tick! It does not correct for the time of the cb execution
            time.sleep(1)
            self.time += 1
            print(f"** Time = {self.time}")

            # For each coroutine
            for task, cor in self.tasks.items():
                # Skip if done
                if task.is_done():
                    continue
                # Advance the coroutine, passing the time
                try:
                    wait = cor.send(self.time)
                    #print(f"** Task {task.name} needs to wait {wait} sec")
                except StopIteration as exception:
                    #print(exception.value)
                    pass

def task1_cb():
    print("Task1 done! 5 secs passed")

def task2_cb():
    print("Task2 done! 2 secs passed")

def task3_cb():
    print("Task3 done! 10 secs passed")


EventLoop().register_task(
    Task(
        name="Task1",
        wait=5,
        cb=task1_cb
    )
).register_task(
    Task(
        name="Task2",
        wait=2,
        cb=task2_cb
    )
).register_task(
    Task(
        name="Task3",
        wait=10,
        cb=task3_cb
    )
).run()

