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

class User:
    def __init__(self, **kwargs):
        self.uid = kwargs.get("uid", None)
        self.email = kwargs.get("email", None)

    def get_uid(self):
        return self.uid

    def write(self):
        m = {'uid': self.uid, 'email': self.email}
        user = us_users.new_item(attrs=m)
        user.put()
        m = {'email': self.email, 'uid': self.uid}
        user = us_email_to_uid.new_item(attrs=m)
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
