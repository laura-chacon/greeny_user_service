import falcon
import falcon.testing as testing
import uuid
import main
import json
from model.user import User
from types import UnicodeType
import model.user

class TestUsers(testing.TestBase):
    def before(self):
        self.api = main.create_api()

    def test_user_found(self):
        uid = str(uuid.uuid4())
        email = "laura@gmail.com"
        next_action_id = str(uuid.uuid4())
        body_req = {'email': email}
        user = User(uid=uid, email=email, next_action_id=next_action_id)
        user.write()
        body = self.req(body_req)
        users = json.loads(body)['users']
        self.assertEqual(1, len(users))
        self.assertEqual(uid, users[0]['uid'])
        self.assertEqual(self.srmock.status, falcon.HTTP_200)

    def test_user_not_found(self):
        uid = str(uuid.uuid4())
        email = "hola@gmail.com"
        body_req = {'email': email}
        body = self.req(body_req)
        body = json.loads(body)
        self.assertEqual(0, len(body['users']))
        self.assertEqual(2, len(body))
        self.assertNotEqual(uid, body['uid'])
        self.assertEqual(self.srmock.status, falcon.HTTP_200)

    def req(self, body):
        headers = [('Accept', 'application/json'),
                       ('Content-Type', 'application/json'),]
        return self.simulate_request('/users/',
                                     headers=headers,
                                     decode='utf-8',
                                     method="GET",
                                     body=json.dumps(body))
