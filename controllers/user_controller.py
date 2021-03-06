import falcon
import sys
import json
import uuid
import requests
from model.user import User

class UserController(object):
    def on_put(self, req, resp, uid):
        email = req.context['body'].get('email')
        password = req.context['body'].get('password')
        next_action_id = "0-" + str(uuid.uuid4().int)
        user = User(uid=uid, email=email, next_action_id=next_action_id)
        user.write()
        r = requests.post(
            "http://127.0.0.1:8002/users/" + str(uid) + "/create_token",
            headers={"Content-Type": "application/json",
                     "Accept": "application/json"}
        )
        auth_token = json.loads(r.content)['auth_token']
        r = requests.put(
            "http://127.0.0.1:8002/users/" + str(uid) + "/password",
            data=json.dumps({"password": password}),
            headers={"Content-Type": "application/json",
                     "Accept": "application/json"}
        )
        req.context['result'] = {'auth_token': auth_token}
        resp.status = falcon.HTTP_200
