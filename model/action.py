import json
import boto
import boto.dynamodb
import os


conn = boto.dynamodb.connect_to_region(
        'eu-west-1',
        aws_access_key_id = os.environ['ACCESS_KEY_ID'],
        aws_secret_access_key = os.environ['SECRET_ACCESS_KEY'])
us_actions = conn.get_table('us_actions')

class Action:
    def __init__(self, **kwargs):
        self.uid = kwargs.get("uid", None)
        self.action_id = kwargs.get("action_id", None)
        self.action_type = kwargs.get("action_type", None)
        self.datetime = kwargs.get("datetime", None)
        self.section = kwargs.get("section", None)
        self.score = kwargs.get("score", None)

    def get_uid(self):
        return self.uid

    def get_actionid(self):
        return self.action_id

    def get_datetime(self):
        return self.datetime

    def write(self):
        m = {
            'uid': self.uid,
            'action_id': self.action_id,
            'action_type': self.action_type,
            'datetime': self.datetime,
            'section': self.section,
            'score': self.score
        }
        action = us_actions.new_item(attrs=m)
        action.put()


def read_by_actionid(action_id):
    try:
        m = us_actions.get_item(action_id)
        return Action(**m)
    except boto.dynamodb.exceptions.DynamoDBKeyNotFoundError:
        return None
