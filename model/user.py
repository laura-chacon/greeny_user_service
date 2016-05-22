import json
import boto3
import boto.dynamodb
import os
from botocore.exceptions import ClientError

client = boto3.resource(
    'dynamodb',
    region_name='eu-west-1',
    aws_access_key_id=os.environ['ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['SECRET_ACCESS_KEY']
)

us_email_to_uid = client.Table('us_email_to_uid')
us_users = client.Table('us_users')
us_uid_to_next_action_id = client.Table('us_uid_to_next_action_id')

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
        if self.email != None:
            us_users.put_item(
                Item={
                    'uid': self.uid,
                    'email': self.email
                }
            )
            us_email_to_uid.put_item(
                Item={
                    'email': self.email,
                    'uid': self.uid
                }
            )
        if self.next_action_id != None:
            us_uid_to_next_action_id.put_item(
                Item={
                    'uid': self.uid,
                    'next_action_id': self.next_action_id
                }
            )


def try_read_by_email(email):
    response = us_email_to_uid.get_item(
        Key={
            'email': email
        }
    )
    if 'Item' in response:
        item = response['Item']
        return User(**item)


def read_by_email(email):
    m = us_email_to_uid.get_item(
        Key={
            'email': email
        }
    )
    m = m['Item']
    return User(**m)

def read_by_next_action_id(uid):
    try:
        m = us_uid_to_next_action_id.get_item(
            Key={
                'uid': uid
            }
        )
        m = m['Item']
        return User(**m)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            print "User already exists"
        else:
            print "Unexpected error: %s" % e

def read_by_uid(uid):
    try:
        m = us_users.get_item(
            Key={
                'uid': uid
            }
        )
        m = m['Item']
        return User(**m)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            print "User already exists"
        else:
            print "Unexpected error: %s" % e


def read_history(uid):
    return None
