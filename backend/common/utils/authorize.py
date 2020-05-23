import json
from functools import wraps

from common.constants import Constants
from common.utils.response import Response
from common.customJWT import CustomJWT
from common.utils.logger import Logger


def authorize():
    """Validate access token and initialize base logger"""

    def authorize_user(func):
        @wraps(func)
        def validate_token(*args, **kwargs):
            logger = Logger(args[0])
            logger.debug("Checking user authentication")
            try:
                body = json.loads(
                    str(args[0]['body']) if args[0].get('body') else json.dumps(args[0].get("queryStringParameters")))
                if not body:
                    return Response().error_response(Constants.BAD_REQUEST,
                                                     Constants.BAD_REQUEST)
                body["access"] = CustomJWT().decode_token(token=args[0]['headers']['Authorization'].strip(),
                                                          logger=logger)
                if body.get("access"):
                    logger.user_id = body["access"].get("user_id", "N0-USERID")
                    return func(body, logger, **kwargs)

                logger.error("Invalid Authentication Token")
                return Response().error_response(Constants.INVALID_OR_EXPIRED_TOKEN,
                                                 Constants.INVALID_OR_EXPIRED_TOKEN)
            except Exception as e:
                logger.exception("auth_exception ")
                return Response().error_response(Constants.INVALID_OR_EXPIRED_TOKEN, Constants.INVALID_OR_EXPIRED_TOKEN)

        return validate_token

    return authorize_user


def no_auth_login():
    """Validate access token and"""

    def login_user_helper(func):
        @wraps(func)
        def initialize_logger(*args, **kwargs):
            logger = Logger(args[0])
            logger.info("User logging in")
            # body = json.loads(args[0]['body'])
            body = json.loads(
                str(args[0]['body']) if args[0].get('body') else json.dumps(args[0].get("queryStringParameters")))

            return func(body, logger, **kwargs)

        return initialize_logger

    return login_user_helper
