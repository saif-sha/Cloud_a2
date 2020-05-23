import sys

sys.path.append("/opt")
from common.utils.response import Response
from common.constants import Constants
from user_common import User
from common.utils.validate_json import validate_json
from common.utils.authorize import no_auth_login

schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",

    "type": "object",
    "properties": {
        "email": {"type": "string", "minLength": 3},
        "password": {"type": "string", "minLength": 3},
    },
    "required": ["email", "password"]

}


@no_auth_login()
@validate_json(schema)
def lambda_handler(event, logger):
    response = Response(logger=logger)
    try:
        user = User(logger, response, event)
        return user.sign_in()
    except Exception as e:
        logger.exception("Unknown exception occurred while login user {}".format(e))
        return response.error_response(Constants.SERVER_ERROR, Constants.SERVER_ERROR)