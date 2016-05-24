import falcon
import falcon.testing as testing
import uuid
import main
import json
from model.user import User
from model.action import Action
import model.action
from types import UnicodeType
import model.user
import datetime

date_handler = lambda obj: (
    obj.isoformat()
    if isinstance(obj, datetime.datetime)
    or isinstance(obj, datetime.date)
    else None
)

class TestGetActionHistory(testing.TestBase):
    def before(self):
        self.api = main.create_api()

    def test_get_action_history(self):
        uid = "123"
        email = "foo@gmail.com"
        next_action_id = "2-789"
        user = User(uid=uid, email=email, next_action_id=next_action_id)
        user.write()
        action_id = "44-sda7d8as6"
        action_type = "foo"
        date = json.dumps(datetime.date.today(), default=date_handler)
        section = "bar"
        score = "5"
        action = Action(uid=uid, action_id=action_id, action_type=action_type, datetime=date, section=section, score=score)
        action.write()
        action = Action(uid=uid, action_id="12-as243", action_type=action_type, datetime=date, section=section, score="8")
        action.write()
        body = self.req(uid)
        body = json.loads(body)
        user_history = body['user_history']
        print user_history
        self.assertEqual(self.srmock.status, falcon.HTTP_200)


    def req(self, uid):
        headers = [('Accept', 'application/json'),
                   ('Content-Type', 'application/json'),]
        return self.simulate_request('/users/' + uid + '/history',
                                     headers=headers,
                                     decode='utf-8',
                                     method="GET")
