import falcon
import falcon.testing as testing
import uuid
import main
import json
from model.user import User
from types import UnicodeType
import model.user

class TestGetNextActionId(testing.TestBase):
    def before(self):
        self.api = main.create_api()

    def test_get_next_action_id(self):
        uid = str(uuid.uuid4())
        email = "lau@gmail.com"
        next_action_id = str(uuid.uuid4())
        user = User(uid=uid, email=email, next_action_id=next_action_id)
        user.write()
        body = self.req(uid)
        body = json.loads(body)
        self.assertEqual(next_action_id, body['next_action_id'])
        self.assertEqual(1, len(body))
        self.assertEqual(self.srmock.status, falcon.HTTP_200)

    def req(self, uid):
        headers = [('Accept', 'application/json'),
                   ('Content-Type', 'application/json'),]
        return self.simulate_request('/users/' + uid + '/actions/next_id',
                                     headers=headers,
                                     decode='utf-8',
                                     method="GET",
                                     body="")
