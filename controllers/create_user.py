import falcon
import sys
import json
from model.user import User

class create_user(object):
    def on_put(self, req, resp, uid):
        email = req.context['body'].get('email')
        new_user = User(uid, email)
        new_user.create(new_user.uid, new_user.email)
        """
        req.context['result'] = result
        resp.status = falcon.HTTP_200
        """
