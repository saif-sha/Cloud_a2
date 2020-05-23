"""
Common logger
USAGE:
logger = Logger(event="LAMBDA EVENT OBJECT", user_id = "user-ID")
logger = Logger(event="LAMBDA EVENT OBJECT", user_id = "user-ID")
logger.info("helloword")

"""

import json
import logging
import os

class Logger(logging.LoggerAdapter):
    user_id = "N0-USERID"

    def __init__(self, event, stage="dev", user_id="N0-USERID", name="assignment"):
        self.user_id = user_id
        # logging.setLoggerClass(MyLogger)
        logging.basicConfig(
            format='%(levelname)s|%(message)s')
        self.event = event
        self.stage = stage
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO if (os.environ.get("stage") == "prod") else logging.DEBUG)
        logger.info('Event | {}'.format(json.dumps(event)))
        super(Logger, self).__init__(logger, user_id)

    def process(self, msg, kwargs):
        return '[{}] {}'.format(self.user_id, msg), kwargs

    def info(self, msg, *args, **kwargs):
        # msg = msg + ' '.join(list(map(str, args)))
        return super(Logger, self).info(msg)
