from session import app
from flask import request, session, g, redirect, url_for, abort, \
                  render_template, flash, make_response, jsonify
import os, json
from models import db, Session, Users_s1
db.init_app(app)


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        user = Users_s1.query.filter_by(login=request.form['login']).first()
        if user is not None:
            if user.password ==  request.form['password']:
                sess = Session(user.user_id)
                db.session.add(sess)
                db.session.commit()
                data = {'userid': str(user.user_id), 'key': sess.key}
                code = 200
            else:
                data = {'error': {'code' : code, 'message' : 'Bad request', 'information' : 'Incorrect credentials'}}
                code = 400
        else:
           data = {'error': {'code' : code, 'message' : 'Bad request', 'information' : 'Incorrect credentials'}}
           code = 400

    return json.dumps(data), code


@app.route('/logout', methods=['POST'])
def logout():
    key =  request.json.get('key')
    code = 400
    if key is not None:
        sess = Session.query.filter_by(key=key).first()
        if sess is not None:
            db.session.delete(sess)
            db.session.commit()
            data = {'message': 'ok', 'code': 200}
        else:
            data = {'error' : {'code' : code, 'message' : 'Bad request', 'information' : 'Unrecognized key value'}}
    else:
        data = {'error' : {'code' : code, 'message' : 'Bad request', 'information' : 'Incorrect parameters'}}
        
    return json.dumps(data), code


@app.route('/status')
def chkuser():
    key = request.json.get('key')
    code = 400
    if key is not None:
        sess = Session.query.filter_by(key=key).first()
        if sess is not None:
            data = {'userid': sess.user_id}
            code = 200
        else:
            data = {'error' : {'code' : code, 'message' : 'Bad request', 'information' : 'Unrecognized key value'}}
    else:
        data = {'error' : {'code' : code, 'message' : 'Bad request', 'information' : 'Incorrect parameters'}}

    return json.dumps(data) code