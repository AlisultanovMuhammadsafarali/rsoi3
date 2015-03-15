from backend1 import app
from flask import request, redirect, url_for, abort

import json
from models import db, Users
db.init_app(app)


@app.route('/signup', methods=['POST'])
def signup():
    code = 400
    data = {'error': {'message': 'Bad request'}}
    if request.method == 'POST':
        userid = request.json.get('userid')
        username = request.json.get('username')
        email = request.json.get('email')
        phone = request.json.get('phone')
        if userid and username and email and phone is not None:
            user = Users(userid, username, email, phone)
            db.session.add(user)
            db.session.commit()
            code = 200
            data = {'message': 'ok'}

    return json.dumps(data), code


@app.route('/me', methods=['GET'])
def me():
    code = 400
    if request.method == 'GET':
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