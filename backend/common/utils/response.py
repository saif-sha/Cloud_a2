import decimal
import json
import logging


class DataEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        if isinstance(o, bytes):
            return str(o, 'utf-8')
        return super(DataEncoder, self).default(o)


class Response:
    def __init__(self, logger=None):
        self.logger = logger if logger else logging
        self.code = {
            "SUCCESS": 200,
            "BAD_REQUEST": 400,
            "UNAUTHORIZED": 401,
            "FORBIDDEN": 403,
            "NOT_FOUND": 404,
            "CONFLICT": 409,
            "PRECONDITION_FAILED": 412,
            "TOO_MANY_REQUESTS": 429,
            "SERVER_ERROR": 500,
            "BAD_GATEWAY": 502,
            "SERVICE_UNAVAILABLE": 503,
            "GATEWAY_TIMEOUT": 504,
            "EMAIL_ALREADY_EXISTS": 409,
            "USERNAME_ALREADY_EXISTS": 409,
            "MULTI_STATUS": 207,
            "EXPECTATION_FAILED": 417,
            "INVALID_OR_EXPIRED_TOKEN": 498
        }
        self.message = {
            "SUCCESS": 'success',
            "BAD_REQUEST": 'bad request',
            "UNAUTHORIZED": 'unauthorized',
            "FORBIDDEN": 'forbidden',
            "CONFLICT": 'conflict',
            "NOT_FOUND": 'not found',
            "SERVER_ERROR": 'internal server error',
            "USERNAME_PASSWORD_MISMATCH": 'invalid username or password',
            "INVALID_JSON_FORMAT": 'invalid json format',
            "INVALID_CURRENT_PASSWORD": "Invalid current password",
            "BAD_GATEWAY": 'bad gateway',
            "GATEWAY_TIMEOUT": 'gateway timeout',
            "TOO_MANY_REQUESTS": 'too many requests',
            "SERVICE_UNAVAILABLE": 'service unavailable',
            "EMAIL_ALREADY_EXISTS": 'email already exists',
            "USERNAME_ALREADY_EXISTS": 'username already exists',
            "PASSWORD_AND_CONFIRM_PASSWORD_NOT_SAME": 'new password and confirm new password are not same',
            "PASSWORD_AND_NEW_PASSWORD_CANT_NOT_BE_SAME": 'password and new password can not be same',
            "PRECONDITION_FAILED": 'precondition failed',
            "INVALID_OR_EXPIRED_TOKEN": 'invalid or expired token',
            "EXPECTATION_FAILED": 'method performed, support actions not saved',
            "NOT_AUTHENTIC_DEVICE": "Device is not authentic Cielo device",
            "DEVICE_ALREADY_EXISTS": "Device is already registered",
            "DEVICE_MAX_COUNT_REACHED": "Maximum device count reached",
            "DEVICE_NAME_ALREADY_EXISTS": "Device with same name already registered",
            "MULTI_STATUS": "MULTI_STATUS",
            "INSERT_QUERY_FAILED": "INSERT_QUERY_FAILED"
        }
        self.reason = [
            "Undefined",
            'invalid or expired token',
            'this user is not exists in db',
            'time zone was invalid',
            'unable to update table',
            'user is not cielo admin user'
        ]

    def get_response_headers(self):
        """
        Add headers for help in allowing all origin in CORS
        :return:
        """
        return {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Allow": "GET, POST, PUT, DELETE, OPTIONS, HEAD",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, HEAD",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": True
        }

    def error_response(self, code, message='', reason=0, data={}, custom_message=None):
        """
        Prepare the response matching old response schema
        :param code: HTTP status code
        :param message: message for body
        :param reason: reason of the error
        :param data: if any json data is returned
        :param custom_message: if user expects other message then default message
        :return:
        """
        resp_body = {
            "error": {
                "code": self.code[code],
                "message": custom_message if custom_message else self.message.get(message, message)
            }
        }

        if reason:
            resp_body['error']['reason'] = self.reason[reason]
        if data:
            resp_body['error']['data'] = data
        resp = {'statusCode': self.code[code], 'body': json.dumps(resp_body),
                "headers": self.get_response_headers()}
        self.logger.error("Response: {}".format(resp))
        return resp

    def success_response(self, message="SUCCESS", data={}, custom_message=None):
        """
        Prepares the success response
        :param message: Message string to get default message
        :param data: if user expects data
        :param custom_message: if user expects other message then default message
        :return:
        """
        # data['internal_users']['user_level']=0
        body = {
            'status': self.code[message],
            'message': custom_message if custom_message else 'success',
            'data': data
        }
        resp = {'statusCode': self.code['SUCCESS'], 'body': json.dumps(body, cls=DataEncoder),
                'headers': self.get_response_headers()}
        self.logger.info("Response: {}".format(resp))
        return resp
