from functools import wraps

from jsonschema import validate, ValidationError

from common.utils.response import Response


def validate_json(schema=None):
    """Validate input data regardless of the content type whether its a valid json or not"""

    def json_decorator(func):
        @wraps(func)
        def json_validator(*args, **kwargs):
            logger = args[1]
            response = Response(logger)
            logger.debug("validating json", args[0])
            event = args[0]
            if not event:
                logger.info("Found empty request body")
                return response.error_response(code="BAD_REQUEST", custom_message="Found Empty Body")
            if schema:
                try:
                    validate(event, schema)
                except ValidationError as e:
                    logger.info("INVALID_REQUEST: {} {} ".format(str(e.path)[7:-2], str(e.message)))
                    return response.error_response(
                        code="BAD_REQUEST",
                        custom_message="INVALID_REQUEST: {} {} ".format(str(e.path)[7:-2], str(e.message))
                    )
            return func(*args, **kwargs)

        return json_validator

    return json_decorator


def validate_query_params(schema=None):
    def query_decorator(func):
        @wraps(func)
        def query_validator(*args, **kwargs):
            logger = args[1]
            response = Response(logger)
            logger.debug("validating json", args[0])
            event = args[0]
            if not event:
                logger.info("No query parameters found")
                return response.error_response(code="BAD_REQUEST", custom_message="Found Empty Body")
            if schema:
                if len(set(schema['required']) - set(event.keys())) == 0:
                    for key in event.keys():
                        try:
                            event[key] = int(event[key]) if (schema['properties'][key] if schema['properties'].get(
                            key) else {}).get('type') == 'number' else event[key]
                        except ValueError:
                            return response.error_response(
                                code="BAD_REQUEST",
                                custom_message="INVALID_REQUEST: Value '{}' in paramter is not integer".format(key)
                            )
                else:
                    result = list(set(schema['required']) - set(event.keys()))
                    return response.error_response(
                        code="BAD_REQUEST",
                        custom_message="INVALID_REQUEST: Properties missing from query parameters. {} ".format(result)
                    )
            return func(*args, **kwargs)

        return query_validator

    return query_decorator
