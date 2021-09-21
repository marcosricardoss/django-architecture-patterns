import json
import uuid
import logging
from dateutil import parser

from app.model import Task
from app.database import db_session as session
logger = logging.getLogger("apieventconsumer")

def task_created_handler(data):    

    entity = json.loads(data['entity'])    
    
    if not session.query(Task).filter_by(public_id=entity["public_id"]).first():
        task = Task()
        task.public_id = entity["public_id"]
        task.title = entity["title"]
        task.description = entity["description"]
        task.deadline_at = parser.parse(entity["deadline_at"])
        task.finished_at = parser.parse(entity["finished_at"]) if entity["finished_at"] else None        
        session.add(task)
        session.commit()

        logger.debug("task created: " + str(entity))
    else:
        logger.debug("this task has already been added before: " + str(entity))
