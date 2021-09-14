import logging

logger = logging.getLogger("webeventconsumer")

def send_task_notification(data):
    logger.debug(
        f""" 
to: manager@email.com
data: {data}"""
    )
