import sys

sys.path.append("/opt")
from common.utils.response import Response
from common.constants import Constants
from user_common import User
from common.utils.validate_json import validate_query_params
from common.utils.authorize import authorize

schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",

    "type": "object",
    "properties": {
        "user_id": {"type": "string", "minLength": 3},
        "email": {"type": "string", "minLength": 3},
        "password": {"type": "string", "minLength": 3},
        "address": {"type": "string", "minLength": 3},
    },
    "required": ["user_id"]

}


@authorize()
@validate_query_params(schema)
def lambda_handler(event, logger):
    response = Response(logger=logger)
    try:
        user = User(logger, response, event)
        return user.update_user()
    except Exception as e:
        logger.exception("Unknown exception occurred while login user {}".format(e))
        return response.error_response(Constants.SERVER_ERROR, Constants.SERVER_ERROR)
