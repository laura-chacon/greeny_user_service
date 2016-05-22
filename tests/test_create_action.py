import falcon
import falcon.testing as testing
import uuid
import main
import json
from model.user import User
from types import UnicodeType
import model.user
from model.action import Action
import model.action
import datetime

date_handler = lambda obj: (
    obj.isoformat()
    if isinstance(obj, datetime.datetime)
    or isinstance(obj, datetime.date)
    else None
)

class TestCreateAction(testing.TestBase):
    def before(self):
        self.api = main.create_api()

    def test_success_create_action(self):
        uid = "7777"
        email="lauraaa@gmail.com"
        next_action_id = "789"
        action_id = "456"
        action_type = "foo"
        date = json.dumps(datetime.date.today(), default=date_handler)
        section = "bar"
        score = 5
        body_req = {'section': section, 'action_type': action_type, 'score': score}
        body = self.req(uid, action_id, body_req)
        body = json.loads(body)
        action = model.action.read(uid, action_id)
        user = model.user.read_by_uid(action.get_uid())
        self.assertEqual(uid, action.get_uid())
        self.assertEqual(date, action.get_datetime())
        self.assertNotEqual(next_action_id, user.get_next_action_id())
        self.assertEqual(self.srmock.status, falcon.HTTP_200)

    def req(self, uid, action_id, body):
        headers = [('Accept', 'application/json'),
                   ('Content-Type', 'application/json'),]
        return self.simulate_request('/users/' + uid + '/actions/' + action_id,
                                     headers=headers,
                                     decode='utf-8',
                                     method="PUT",
                                     body=json.dumps(body))
