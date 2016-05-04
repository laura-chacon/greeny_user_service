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
        uid = "123"
        email="lauraaa@gmail.com"
        next_action_id = "789"
        action_id = "456"
        action_type = "foo"
        date = json.dumps(datetime.date.today(), default=date_handler)
        section = "bar"
        score = 5
        action = Action(uid=uid, action_id=action_id, action_type=action_type, datetime=date, section=section, score=score)
        action.write()
        user = User(uid=uid, email=email, next_action_id=next_action_id)
        user.write()
        body_req = {'section': section, 'action_type': action_type, 'score': score}
        body = self.req(uid, action_id, body_req)
        body = json.loads(body)
        user = model.user.read_by_uid(uid)
        action = model.action.read_by_actionid(action_id)
        self.assertEqual(user.get_uid(), action.get_uid())
        self.assertEqual(date, action.get_datetime())
        self.assertEqual(email, user.get_email())
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
