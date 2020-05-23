import sys

sys.path.append("/opt")
from common.utils.response import Response
from common.constants import Constants
from weather_common import Weather
from common.utils.validate_json import validate_json
from common.utils.authorize import authorize

schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",

    "type": "object",
    "properties": {
        "filename": {"type": "string", "minLength": 3},

    },
    "required": ["filename"]

}


@authorize()
@validate_json(schema)
def lambda_handler(event, logger):
    response = Response(logger=logger)
    try:
        weather = Weather(logger, response, event)
        return weather.get_profilepicture_url()
    except Exception as e:
        logger.exception("Unknown exception occurred while add schedule {}".format(e))
        return response.error_response(Constants.SERVER_ERROR, Constants.SERVER_ERROR)



