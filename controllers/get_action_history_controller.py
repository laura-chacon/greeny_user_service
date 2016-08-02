import falcon
import sys
import json
import uuid
import requests
from model.user import User
import model.user
import datetime

class GetActionHistoryController(object):
    def on_get(self, req, resp, uid):
        def f(x):
            x['score'] = int(x['score'])
            return x
        user_history = model.user.read_history(uid)
        user_history = map(f, user_history)
        req.context['result'] = {'user_history': user_history}
        resp.status = falcon.HTTP_200
