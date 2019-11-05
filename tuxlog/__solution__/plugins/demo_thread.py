from common.app import socketio
import logging

logger = logging.getLogger(__name__)

thread=None

def task():
    while True:
        logger.info("hello from long running task")        
        socketio.sleep(1)

def register():
    global thread
    thread=socketio.start_background_task(task)
    logger.info("started")
