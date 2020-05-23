import datetime
import time

import boto3
import requests
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

AWS_REGION = "ap-southeast-2"
client = boto3.client('ses',
                      aws_access_key_id='AKIA6D4BINLHF47VPKJG',
                      aws_secret_access_key='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',
                      region_name=AWS_REGION)
CHARSET = "UTF-8"

dynamo_db = boto3.resource('dynamodb',
                           aws_access_key_id='AKIA6D4BINLHF47VPKJG',
                           aws_secret_access_key='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',
                           region_name='ap-southeast-2')
user_schedule = dynamo_db.Table("schedule")
user = dynamo_db.Table("user")


def get_current_temp(lat, lon):
    url = "https://weatherbit-v1-mashape.p.rapidapi.com/current"

    querystring = {"lang": "en", "lon": lon, "lat": lat}

    headers = {
        'x-rapidapi-host': "weatherbit-v1-mashape.p.rapidapi.com",
        'x-rapidapi-key': "7ea6b01a87msh20639a7f034b400p19f866jsn93d528df4107"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response.json()


def get_upcoming_notification():
    mytime = get_time()
    print(mytime)
    all_schedules = user_schedule.scan(FilterExpression=Key("notification_time").between(mytime, mytime + 60))
    if all_schedules["Count"] > 0:
        for one_schedule in all_schedules["Items"]:
            specific_user = user.get_item(Key={"user_id": one_schedule["user_id"]})
            RECIPIENT = specific_user["Item"]["email"]
            print("Sending email to {}".format(RECIPIENT))
            lat = one_schedule['lat']
            lon = one_schedule['lon']
            temp = get_current_temp(lat, lon)
            SUBJECT = "Weather for {} is {}".format(one_schedule["area"], temp['data'][0]['temp'])
            BODY_TEXT = ("Temperature According to your schedule for area {} is {} Celcius.".format(one_schedule["area"], temp['data'][0]['temp']))

            BODY_HTML = """<html>
            <head></head>
            <body>
              <h1>Temperature According to your schedule for area {} is {} Celcius.</h1>
              <p>Sent by SES</p>
            </body>
            </html>
                        """.format(one_schedule["area"], temp['data'][0]['temp'])

            try:
                response = client.send_email(
                    Destination={
                        'ToAddresses': [
                            RECIPIENT,
                        ],
                    },
                    Message={
                        'Body': {
                            'Html': {
                                'Charset': CHARSET,
                                'Data': BODY_HTML,
                            },
                            'Text': {
                                'Charset': CHARSET,
                                'Data': BODY_TEXT,
                            },
                        },
                        'Subject': {
                            'Charset': CHARSET,
                            'Data': SUBJECT,
                        },
                    },
                    Source="WeatherNotification@rmitassignment.tk",
                )
            except ClientError as e:
                print(e.response['Error']['Message'])
            else:
                user_schedule.delete_item(Key={"user_id":one_schedule["user_id"], "schedule_id":one_schedule["schedule_id"]}, ReturnValues="NONE")
                print("Email sent! Message ID:"),
                print(response['MessageId'])


def get_time():
    unix_epoch = datetime.datetime(1970, 1, 1)
    log_dt = datetime.datetime.strptime(datetime.datetime.utcnow().strftime("%y-%m-%d %H:%M:%S."), "%y-%m-%d %H:%M:%S.")
    seconds_from_epoch = (log_dt - unix_epoch).total_seconds()
    return int(seconds_from_epoch)


while True:
    print("Checking for pending notification")
    get_upcoming_notification()
    time.sleep(60)
