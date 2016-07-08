import falcon
import sys
import uuid
import json
from model.user import User
import model.user
import urlparse

class UsersController(object):
    def on_get(self, req, resp):
        query_string = req.query_string
        email = urlparse.parse_qs(query_string)['email'][0]
        user = model.user.try_read_by_email(email)
        if user == None:
            new_uid = str(uuid.uuid4())
            body = {'users': [], 'uid': new_uid}
        else:
            uid = user.get_uid()
            body = {'users': [{'uid': uid}]}
        req.context['result'] = body
        resp.status = falcon.HTTP_200
