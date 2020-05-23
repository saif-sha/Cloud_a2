import logging

import boto3
from boto3.dynamodb.conditions import Key

from botocore.exceptions import ClientError

class Table:
    """
    A generic Table helper
    """
    def make_key_expression(self, dictionary):
        key_expression = None
        for key in list(dictionary.keys()):
            if key_expression:
                key_expression = key_expression & Key(key).eq(dictionary[key])
            else:
                key_expression = Key(key).eq(dictionary[key])
        return key_expression

    def __init__(self, table_name, logger=None):
        self.logger = logger if logger else logging
        self.table_name = table_name
        self.dynamo_db = boto3.resource('dynamodb')
        self.table = self.dynamo_db.Table(self.table_name)

    def createTableObject(self, dynamo_db):
        self.table = dynamo_db.Table(self.table_name)

    def get_table_object(self):
        return self.table

    def getTargetDynamodbResource(self, table_name, aws_access_key_id,
                                  aws_secret_access_key, region_name="us-west-2", aws_session_token=None):
        dynamo_db = boto3.resource('dynamodb', region_name=region_name,
                                   aws_access_key_id=aws_access_key_id,
                                   aws_secret_access_key=aws_secret_access_key,
                                   aws_session_token=aws_session_token)
        self.table_name = table_name
        self.createTableObject(dynamo_db)
        return self

    def getDynamodbResource(self, table_name, aws_access_key_id, aws_secret_access_key, region_name="us-east-1"):
        dynamo_db = boto3.resource('dynamodb', region_name=region_name,
                                   aws_access_key_id=aws_access_key_id,
                                   aws_secret_access_key=aws_secret_access_key)
        self.table_name = table_name
        self.createTableObject(dynamo_db)
        return self

    def put_item_new(self, item):
        self.table.put_item(Item=item)
        self.logger.debug("Class : Table, Function : put_item, Successful")
        return True

    def get_item_by_key(self, key):
        try:
            response = self.table.get_item(Key=key)
            self.logger.debug("Getting item by key, found : {}".format(response.get("Item", None)))
            return response.get("Item", None)
        except ClientError:
            return []


    def get_item_via_query(self, key_expression, index=None, filter_expression=None, limit=None,
                           exclusivestartkey=None, scanindexforward=None, evaluate_key=False):
        query = {"KeyConditionExpression": self.make_key_expression(key_expression)}
        if index is not None:
            query.update({"IndexName": index})
        if filter_expression is not None:
            query.update({"FilterExpression": filter_expression})
        if limit is not None:
            query.update({"Limit": limit})
        if exclusivestartkey is not None:
            query.update({"ExclusiveStartKey": exclusivestartkey})
        if scanindexforward is not None:
            query.update({"ScanIndexForward": scanindexforward})
        response = self.table.query(**query)
        self.logger.debug("getting item via limit query: {}".format(response))
        if response["Count"] > 0:
            last_evaluated_key = response.get('LastEvaluatedKey', {})

            if evaluate_key:
                return response["Items"], last_evaluated_key
            return response["Items"]
        if evaluate_key:
            return [], {}
        else:
            return []

    def update_item_by_key(self, key, update_expression=None, expression_attribute_values=None,
                           condition_expression=None, return_values="NONE", expression_attribute_names=None):
        query = {"Key": key}
        if condition_expression:
            query.update({"ConditionExpression": condition_expression})
        if update_expression:
            query.update({"UpdateExpression": update_expression})
        if expression_attribute_values:
            query.update({"ExpressionAttributeValues": expression_attribute_values})
        if return_values:
            query.update({"ReturnValues": return_values})
        if condition_expression:
            query.update({"ConditionExpression": condition_expression})
        if expression_attribute_names:
            query.update({"ExpressionAttributeNames": expression_attribute_names})

        response = self.table.update_item(**query)
        return response.get("Attributes", None)

    def put_item(self, item, logger):
        try:
            self.table.put_item(Item=item)
            self.logger.debug("Adding new item to database")
            return True
        except Exception as e:
            logger.exception(e)
            return False

    def scan_table(self, filter_expression=None):
        if filter_expression is None:
            result_set = self.table.scan()
        else:
            result_set = self.table.scan(FilterExpression=filter_expression)
        list_item = result_set['Items']
        while 'LastEvaluatedKey' in result_set:
            if filter_expression is None:
                result_set = self.table.scan(ExclusiveStartKey=result_set['LastEvaluatedKey'])
            else:
                result_set = self.table.scan(FilterExpression=filter_expression,
                                             ExclusiveStartKey=result_set['LastEvaluatedKey'])
            list_item += result_set['Items']
        return list_item

    def delete_item_by_key(self, key, return_values):

        response = self.table.delete_item(Key=key, ReturnValues=return_values)
        return response.get("Attributes", None)

    def delete_items_by_batch_writer(self, item_list):

        with self.table.batch_writer() as batch:
            for item in item_list:
                batch.delete_item(Key=item)
        return True

    def put_items_by_batch_writer(self, item_list):

        with self.table.batch_writer() as batch:
            for item in item_list:
                batch.put_item(Item=item)
        return True
