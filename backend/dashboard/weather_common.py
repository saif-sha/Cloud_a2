from common.constants import Constants
from common.customJWT import CustomJWT
from common.database import Table
from common.utils.util import Util


class Weather:

    def __init__(self, logger, response, event):

        self.logger = logger
        self.response = response
        self.event = event
        self.util = Util()
        self.schedule_table = Table(table_name="schedule", logger=self.logger)
        self.user_table = Table(table_name="user", logger=self.logger)

    def add_schedule(self):
        user_id = self.event["access"].get("user_id")
        time = self.event.get("notification_time")
        lat = self.event.get("lat")
        lon = self.event.get("lon")
        area = self.event.get("area")

        new_schedule = {
            "user_id": user_id,
            "schedule_id": self.util.id_generator(),
            "notification_time": time,
            "lat": lat,
            "lon": lon,
            "area": area
        }
        schedule = self.schedule_table.put_item(new_schedule, self.logger)
        if schedule:
            return self.response.success_response(data=new_schedule)
        return self.response.error_response(code=Constants.BAD_REQUEST,
                                            custom_message="invalid data")

    def update_schedule(self):
        user_id = self.event["access"].get("user_id", None)
        schedule_id = self.event.get("schedule_id", None)
        if user_id and schedule_id:
            update_expression = 'SET '
            expression_attribute_values = {}
            for key in self.event:
                if key not in ['user_id', 'schedule_id', 'access'] and self.event[key] != '':
                    update_expression += "{0} = :{0},".format(key)
                    expression_attribute_values[':{}'.format(key)] = self.event[key]
            if update_expression != 'SET ':
                update_expression = update_expression[:-1]

                schedule = self.schedule_table.update_item_by_key(
                    key={"user_id": user_id, "schedule_id":schedule_id}, update_expression=update_expression,
                    expression_attribute_values=expression_attribute_values, return_values="ALL_NEW")

                if schedule:
                    return self.response.success_response(data=schedule)
                return self.response.error_response(code=Constants.NOT_FOUND,
                                                    message=Constants.NOT_FOUND)

        return self.response.error_response(code=Constants.BAD_REQUEST,
                                            custom_message="invalid data")

    def delete_schedule(self):
        user_id = self.event["access"].get("user_id", None)
        schedule_id = self.event.get("schedule_id", None)
        if user_id and schedule_id:
            schedule = self.schedule_table.delete_item_by_key(
                key={"user_id": user_id, "schedule_id": schedule_id}, return_values="ALL_OLD")
            if schedule:
                return self.response.success_response(data=schedule)
            return self.response.error_response(code=Constants.NOT_FOUND,
                                                message=Constants.NOT_FOUND)

        return self.response.error_response(code=Constants.BAD_REQUEST,
                                            custom_message="invalid data")

    def dashboard(self):
        user_id = self.event["access"].get("user_id", None)
        resp = {}
        resp["schedules"] = self.schedule_table.get_item_via_query({"user_id": user_id})
        user = self.user_table.get_item_by_key({"user_id": user_id})
        del user["password"]
        resp["user"]=user
        resp["temperature"]=self.util.get_current_temp(self.event.get("lat"),self.event.get("lon") )
        return self.response.success_response(data=resp)

    def get_profilepicture_url(self):
        user_id = self.event["access"].get("user_id", None)
        pictureName = self.event.get("filename", None)
        self.user = self.user_table.update_item_by_key(
            key={"user_id": user_id}, update_expression="SET profile_picture = :profile_picture",
            expression_attribute_values={":profile_picture":"https://userprofilepicture.s3-ap-southeast-2.amazonaws.com/"+pictureName}, return_values="UPDATED_NEW")
        return self.response.success_response(data={})
