import json
import uuid
import logging
from dateutil import parser

from app.model import Task
from app.database import db_session as session
logger = logging.getLogger("apieventconsumer")

def task_created_handler(data):    
    entity = json.loads(data['entity'])    
    
    task = Task()
    task.public_id = uuid.uuid1().hex
    task.title = entity["title"]
    task.deadline_at = parser.parse(entity["deadline_at"])
    task.created_at = parser.parse(entity["deadline_at"])

    session.add(task)
    session.commit()

    logger.debug("task created: " + str(entity))
