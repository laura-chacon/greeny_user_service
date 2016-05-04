import falcon
import sys
import json
import uuid
import requests
from model.action import Action
import model.action
from model.user import User
import model.user
import datetime

date_handler = lambda obj: (
    obj.isoformat()
    if isinstance(obj, datetime.datetime)
    or isinstance(obj, datetime.date)
    else None
)

class CreateActionController(object):
    def on_put(self, req, resp, uid, action_id):
        section = req.context['body'].get('section')
        action_type = req.context['body'].get('action_type')
        score = req.context['body'].get('score')
        date = json.dumps(datetime.date.today(), default=date_handler)
        action = Action(uid=uid, action_id=action_id, action_type=action_type, datetime=date, section=section, score=score)
        action.write()
        next_action_id = str(uuid.uuid4())
        user = model.user.read_by_uid(uid)
        email = user.get_email()
        user = User(uid=uid, email=email, next_action_id=next_action_id)
        user.write()
        req.context['result'] = {}
        resp.status = falcon.HTTP_200
