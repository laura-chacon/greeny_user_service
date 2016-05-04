import json
import boto
import boto.dynamodb
import os

conn = boto.dynamodb.connect_to_region(
        'eu-west-1',
        aws_access_key_id = os.environ['ACCESS_KEY_ID'],
        aws_secret_access_key = os.environ['SECRET_ACCESS_KEY'])
us_email_to_uid = conn.get_table('us_email_to_uid')
us_users = conn.get_table('us_users')
us_uid_to_next_action_id = conn.get_table('us_uid_to_next_action_id')

class User:
    def __init__(self, **kwargs):
        self.uid = kwargs.get("uid", None)
        self.email = kwargs.get("email", None)
        self.next_action_id = kwargs.get("next_action_id", None)

    def get_uid(self):
        return self.uid

    def get_email(self):
        return self.email

    def get_next_action_id(self):
        return self.next_action_id

    def write(self):
        m = {'uid': self.uid, 'email': self.email}
        user = us_users.new_item(attrs=m)
        user.put()
        m = {'email': self.email, 'uid': self.uid}
        user = us_email_to_uid.new_item(attrs=m)
        user.put()
        m = {'uid': self.uid, 'next_action_id': self.next_action_id}
        user = us_uid_to_next_action_id.new_item(attrs=m)
        user.put()

def try_read_by_email(email):
    try:
        m = us_email_to_uid.get_item(email)
        return User(**m)
    except boto.dynamodb.exceptions.DynamoDBKeyNotFoundError:
        return None

def read_by_email(email):
    m = us_email_to_uid.get_item(email)
    return User(**m)

def read_by_next_action_id(uid):
    try:
        m = us_uid_to_next_action_id.get_item(uid)
        return User(**m)
    except boto.dynamodb.exceptions.DynamoDBKeyNotFoundError:
        return None

def read_by_uid(uid):
    try:
        m = us_users.get_item(uid)
        return User(**m)
    except boto.dynamodb.exceptions.DynamoDBKeyNotFoundError:
        return None
