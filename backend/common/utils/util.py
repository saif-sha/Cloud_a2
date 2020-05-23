from __future__ import print_function
import base64
import logging
import random
import string
import boto3
import json
import re
import smtplib
import requests

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

dynamodb = boto3.resource('dynamodb')
clientS3 = boto3.client('s3')
sesclient = boto3.client('ses')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Util:
    def __init__(self):
        pass

    def encode_base64(self, string):
        """
        author ali
        :param string: string you wants to encode
        :return: return encoded string
        """
        try:
            return base64.b64encode(string.encode('UTF-8')).decode("utf-8")  # will work with python 2 and 3
        except Exception as e:
            self.log(e)
            return None

    def decode_base64(self, string):
        """
        author ali
        :param string: string: string you wants to decode
        :return: return decoded string
        """
        try:
            # return string.decode('base64') # will work with python 2 only
            # return base64.b64decode(string.encode('ascii'))  # will work with python 2 and 3
            # return base64.b64decode(string.encode('ascii'))  # will work with python 2 and 3
            return base64.b64decode(string).decode('UTF-8')  # will work with python 2 and 3
        except Exception as e:
            self.log(e)
            return None

    def id_generator(self, size=32, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
        # one implementation of this moethod in import common.imports.modules.CommonBLLs.ConfigBLL as ConfigBLL too
        return ''.join(random.choice(chars) for _ in range(size))

    def get_bucket_image_path(self, bucket_name, key):
        """
        :param bucket_name: name of S3 bucket
        :param key: user image path
        :return: return image path if found, else will return empty string
        """
        try:
            s3_response = clientS3.get_object(Bucket=bucket_name, Key=key)
            strm = s3_response['Body']
            strm_str = strm.read()
            return self.encode_base64(strm_str)
        except Exception as e:
            self.log(e)
            return self.EMPTY_STRING

    def is_valid_email(self, email):
        """
        author ali
        :param email: is the string yu wants to verify
        :return: rue if match else False
        """
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', str(email).lower())
        if match is None:
            return False
        return True

    def is_valid_username(self, username):
        """
        author ali
        :param username: is the string yu wants to verify
        :return: rue if match else False
        """
        match = re.match('^(?=.{5,25}$)(?![_.-])[a-zA-Z0-9._-]+(?<![_.-])$', username)
        if match is None:
            return False
        return True

    def is_valid_password(self, password):
        """
        author ali
        :param password: is the string yu wants to verify
        :return: True if match else False
        """
        match = re.match('^.{5,15}$', password)
        if match is None:
            return False
        return True

    def send_mail(self, subject, message, reciever, invitee, sender='noreply@virtualrestaurantmanager.com'):
        try:
            server = smtplib.SMTP_SSL('virtualrestaurantmanager.com', 465)
            server.ehlo()
            server.login(sender, 'noreply@123x')
            msg = MIMEMultipart(message)
            msg['From'] = sender
            msg['To'] = reciever
            msg['Subject'] = subject
            body = MIMEText(message.format(invitee))
            msg.attach(body)
            server.sendmail(sender, reciever, msg.as_string())
            server.close()
        except Exception as e:
            import logging
            logging.exception(e)
            print('Something went wrong...')

    def get_current_temp(self, lat, lon):

        url = "https://weatherbit-v1-mashape.p.rapidapi.com/current"

        querystring = {"lang": "en", "lon": lon, "lat": lat}

        headers = {
            'x-rapidapi-host': "weatherbit-v1-mashape.p.rapidapi.com",
            'x-rapidapi-key': "7ea6b01a87msh20639a7f034b400p19f866jsn93d528df4107"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        return response.json()

    def get_upload_signed_url(self, key):
        s3 = boto3.client('s3')
        presigned_url = s3.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': "userprofilepicture",
                'Key': key
            },
            HttpMethod='PUT'
        )
        return presigned_url


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
