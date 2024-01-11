import asyncio
import queue 
import time 
from dataclasses import dataclass
from uuid import uuid4
from datetime import datetime, timedelta
from typing import Optional, Sequence


@dataclass
class Task:
    _id: uuid4 = None
    instance: object = None
    name: str = None
    start_time: datetime = None
    end_time: Optional[datetime] = None 
    status: str = 'created'


new_tasks_queue = queue.Queue()
tasks: Sequence[Task]  = []
keep_running_task_manager: bool = True
max_timeout_seconds = 5*60  # 5 minutes = 300 seconds


async def push_task(task):
    new_tasks_queue.put(task)


async def x():
    print("XXXXXX")
    await asyncio.sleep(20)  
    print("Done XXX")


async def y():
    print("YYYYYY")
    await asyncio.sleep(2)  
    print("Done YYYY")


async def get_tasks_status():
    print("-------")
    for task in tasks:
        print("> ", task.name, task._id, task.start_time, task.status)


async def create_task(loop, task_func):
    listener_task = loop.create_task(task_func())
    return listener_task


async def hear_new_tasks():
    loop = asyncio.get_event_loop()
    # simulate task coming from API!
    await push_task("x")
    await push_task("get_tasks_status")
    await push_task("z")
    await push_task("get_tasks_status")
    await push_task("y")

    while True:
        if not new_tasks_queue.empty():
            new_task = new_tasks_queue.get()
            task_mp = {
                "x": x,
                "y": y,
                "get_tasks_status": get_tasks_status,
            }
            task_func = task_mp.get(new_task) or None
            if task_func:
                task_instance = await create_task(loop=loop, task_func=task_func)
                tasks.append(Task(
                    instance=task_instance, 
                    name=new_task,
                    start_time=datetime.utcnow(),
                    _id=uuid4(),
                ))
            else:
                print("Invalid task", task_func)
        
        for task in tasks:
            if task.status == 'created':
                if task.instance._state == 'FINISHED':
                    print(f"{task.name} started at {task.start_time} is done!")
                    task.end_time = datetime.utcnow()
                    task.status = 'finished'
                else:
                    time_difference = datetime.utcnow() - task.start_time 
                    if time_difference >= timedelta(seconds=max_timeout_seconds):
                        # force cancel due timeout!
                        task.status = 'stopped'
                        task.instance.cancel()

        await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(hear_new_tasks())
    print("HERE SHOULD RUN THE API, but asnyc.run takes the entire loop!!")
