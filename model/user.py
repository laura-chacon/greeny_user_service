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
    def __init__(self, uid, email):
        self.uid = uid
        self.email = email

    def get_uid(self, email):
        try:
            uid = us_email_to_uid.get_item(email)['uid']
        except boto.dynamodb.exceptions.DynamoDBKeyNotFoundError:
            uid = None
        return uid

    def create(self, uid, email):
        user = us_users.new_item(
            attrs = {
                'uid': uid,
                'email': email
            }
        )
        user.put()
        user = us_email_to_uid.new_item(
            attrs = {
                'email': email,
                'uid': uid
            }
        )
        user.put()
