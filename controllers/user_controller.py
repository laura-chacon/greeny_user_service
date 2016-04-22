import falcon
import sys
import json
import requests
from model.user import User

class UserController(object):
    def on_put(self, req, resp, uid):
        email = req.context['body'].get('email')
        password = req.context['body'].get('password')
        user = User(uid=uid, email=email)
        user.write()
        r = requests.post(
            "http://127.0.0.1:8002/users/" + str(uid) + "/create_token",
            data=json.dumps({}),
            headers={"Content-Type": "application/json",
                     "Accept": "application/json"})
        token = json.loads(r.content)['token']
        r = requests.put(
            "http://127.0.0.1:8002/users/" + str(uid) + "/password",
            data=json.dumps({"password": password}),
            headers={"Content-Type": "application/json",
                     "Accept": "application/json"}
        )
        req.context['result'] = {'token': token}
        resp.status = falcon.HTTP_200
