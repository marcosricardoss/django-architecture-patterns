import logging

logger = logging.getLogger("django")

def send_mail(*args, **kwargs):    
    logger.info(f"SENDING EMAIL: {args}")