import falcon
import falcon.testing as testing
import uuid
import main
import json
from model.user import User
from types import UnicodeType
import model.user
from mock import MagicMock
from mock import patch
import requests

class TestUser(testing.TestBase):
    def before(self):
        self.api = main.create_api()

    @patch('requests.post')
    @patch('requests.put')
    def test_put_user(self, mock_requests_put, mock_requests_post):
        mock_requests_post.return_value = TestUser.MockResponse('{"auth_token": "abc"}')
        mock_requests_put.return_value = TestUser.MockResponse('')
        uid = str(uuid.uuid4())
        email = "laurac@gmail.com"
        password = str(uuid.uuid4())
        body = {'email': email, 'password': password}
        body = self.req(uid, body)
        token = json.loads(body)['auth_token']
        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        user = model.user.read_by_email(email)
        self.assertEqual(uid, user.get_uid())
        self.assertEqual("abc", token)

# TODO: handle case where auth_service.put_password doesn't return 200


    def req(self, uid, body):
        headers = [('Accept', 'application/json'),
                       ('Content-Type', 'application/json'),]
        return self.simulate_request('/users/' + uid,
                                     headers=headers,
                                     decode='utf-8',
                                     method="PUT",
                                     body=json.dumps(body))

    class MockResponse:
        def __init__(self, content):
            self.content = content
