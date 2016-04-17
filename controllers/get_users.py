import falcon
import sys
import uuid
import json
from model.user import User

class get_users(object):
    def on_get(self, req, resp):
        email = req.get_param('email')
        new_user = User(None, email)
        uid = new_user.get_uid(email)
        users = list()
        if uid == None:
            new_uid = str(uuid.uuid4())
            body = {'users': users, 'uid': new_uid}
        else:
            users.append(uid)
            body = {'users': users}
        resp.body = json.dumps(body)
        resp.status = falcon.HTTP_200
