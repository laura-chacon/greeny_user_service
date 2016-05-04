import json
import boto
import boto.dynamodb
import os


conn = boto.dynamodb.connect_to_region(
        'eu-west-1',
        aws_access_key_id = os.environ['ACCESS_KEY_ID'],
        aws_secret_access_key = os.environ['SECRET_ACCESS_KEY'])
us_actions = conn.get_table('us_actions')
us_uid_to_next_action_id = conn.get_table('us_uid_to_next_action_id')

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
