from common.constants import Constants
from common.customJWT import CustomJWT
from common.database import Table
from common.utils.util import Util


class User:

    def __init__(self, logger, response, event):

        self.logger = logger
        self.response = response
        self.event = event
        self.util = Util()
        self.user_table = Table(table_name="user", logger=self.logger)

    def sign_in(self):
        email = self.event.get("email").lower()
        password = self.event.get("password")
        if self.util.is_valid_email(email) and self.util.is_valid_password(password):
            self.user = self.user_table.get_item_via_query({"email": email}, index="email-index")
            if not self.user:
                return self.response.error_response(code=Constants.UNAUTHORIZED,
                                                    custom_message="invalid email/password")
        else:
            return self.response.error_response(code=Constants.UNAUTHORIZED,
                                                custom_message="invalid email/password")
        password = self.util.encode_base64(password)
        self.logger.info(self.user)
        data = {
            "user_id": self.user[0]["user_id"],
            "email": self.user[0]["email"],
            "address": self.user[0]["address"],
            "profile_picture": self.user[0]["profile_picture"]
        }
        if password == self.user[0].get("password"):
            data['access_token'] = CustomJWT().generate_token(data, logger=self.logger)
            return self.response.success_response(data=data)
        return self.response.error_response(code=Constants.UNAUTHORIZED,
                                            custom_message="invalid email/password")

    def create_user(self):
        email = self.event.get("email")
        password = self.event.get("password")
        if not all([self.util.is_valid_email(email), self.util.is_valid_password(password)]):
            return self.response.error_response(code=Constants.BAD_REQUEST,
                                                custom_message="invalid email/password")

        self.user = self.user_table.get_item_via_query({"email": email}, index="email-index")
        if self.user:
            return self.response.error_response(code=Constants.CONFLICT,
                                                custom_message="email already in use")

        new_user = {
            "user_id": self.util.id_generator(),
            "address": self.event.get("address"),
            "email": self.event.get("email").lower(),
            "password": self.util.encode_base64(self.event.get("password")),
            "profile_picture": self.event.get("profile_picture"),
        }
        self.user = self.user_table.put_item(new_user, self.logger)
        if self.user:
            del new_user['password']
            #TODO: send welcome email
            return self.response.success_response(data=new_user)
        return self.response.error_response(code=Constants.BAD_REQUEST,
                                            custom_message="invalid data")

    def update_user(self):
        user_id = self.event.get("user_id", None)
        if self.event.get("password"):
            self.event['password'] = self.util.encode_base64(self.event.get("password"))
        if user_id:
            update_expression = 'SET '
            expression_attribute_values = {}
            for key in self.event:
                if key not in ['email', 'user_id', 'access'] and self.event[key] != '':
                    update_expression += "{0} = :{0},".format(key)
                    expression_attribute_values[':{}'.format(key)] = self.event[key]
            if update_expression != 'SET ':
                update_expression = update_expression[:-1]

                self.user = self.user_table.update_item_by_key(
                    key={"user_id": user_id}, update_expression=update_expression,
                    expression_attribute_values=expression_attribute_values, return_values="ALL_NEW")

                if self.user:
                    return self.response.success_response(data=self.user)
                return self.response.error_response(code=Constants.NOT_FOUND,
                                                    message=Constants.NOT_FOUND)

        return self.response.error_response(code=Constants.BAD_REQUEST,
                                            custom_message="invalid data")
