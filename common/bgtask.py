import logging

logger = logger = logging.getLogger(__name__)

__backgroud_tasks=dict()

'''
task=thread
'''
def register(unique_name, task):
    if not unique_name in __backgroud_tasks:
        __backgroud_tasks[unique_name]=task


def start_all():
    for unique_name, task in __backgroud_tasks.items():
        if not __is_started(task):
            task.start()
            logger.info(unique_name + " started")

def stop_all():
    for unique_name, task in __backgroud_tasks.items():
        if __is_started(task):
            task.stop()
            logger.info(unique_name + " stoped")

def stop(unique_name):
    if unique_name in __backgroud_tasks:
        task=__backgroud_tasks[unique_name]
        if __is_started(task):
            __backgroud_tasks[unique_name].stop()

def start(unique_name):
    if unique_name in __backgroud_tasks:
        task=__backgroud_tasks[unique_name]
        if not __is_started(task):
            task[unique_name].start()

def get_all():
    result=dict()
    for name, task in __backgroud_tasks.items():
        result[name]=task.name

    return result

def __is_started(task):
    return task._started._flag