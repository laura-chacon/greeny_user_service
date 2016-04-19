import falcon
import sys
import uuid
import json
from model.user import User

class Users(object):
    def on_get(self, req, resp):
        email = req.get_param('email')
        user = User(None, email)
        uid = user.read_uid_from_email()
        if uid == None:
            new_uid = str(uuid.uuid4())
            body = {'users': [], 'uid': new_uid}
        else:
            body = {'users': [{'uid': uid}]}
        req.context['result'] = body
        resp.status = falcon.HTTP_200
