from backend1 import app
from flask import request, session, g, redirect, url_for, abort, \
                  render_template, flash, make_response, jsonify
import json
from models import db, Users
db.init_app(app)


@app.route('/me', methods=['GET'])
def me():
    code = 400
    userid = request.json.get('userid')
    if userid is not None:
        me = Users.query.filter_by().all()
        if me is not None:
            u = []
            for user in me:
                u.append({'username': user.name})
            code = 200
            data = u
        else:
            code=204
            data = {'error': {'code': code, 'message': 'No Content'}}
    else:
        data = {'error': {'code': code, 'message': 'Bad request', 'information': 'Incorrect credentials'}}

    return json.dumps(data), code