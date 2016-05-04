import falcon
import sys
import json
import uuid
import requests
from model.user import User
import model.user

class GetNextActionIdController(object):
    def on_get(self, req, resp, uid):
        user = model.user.read_by_next_action_id(uid)
        next_action_id = user.get_next_action_id()
        req.context['result'] = {'next_action_id': next_action_id}
        resp.status = falcon.HTTP_200
