from session import app
from flask import request, session, g, redirect, url_for, abort, \
                  render_template, flash, make_response, jsonify
import os, json, hashlib
from models import db, Session1, Users_s1, DATE_FORMAT, SESSION_EXPIRE_DAY
from datetime import datetime, timedelta
from sqlalchemy import update

db.init_app(app)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        user = Users_s1.query.filter_by(login=request.json.get('username')).first()
        if user is not None:
            if user.password == request.json.get('password'):
                sess = Session1.query.filter_by(user_id=user.user_id).first()
                if sess is not None:
                    nkey=get_key(user.user_id)
                    sess.key = nkey
                    sess.expire = get_expire()
                    db.session.commit()
                else:
                    sess = Session1(user.user_id)
                    db.session.add(sess)
                    db.session.commit()
                    nkey = sess.key

                data = {'userid': str(user.user_id), 'key': nkey}
                code = 200
            else:
                data = {'error': {'code' : code, 'message' : 'Bad request', 'information' : 'Incorrect credentials'}}
                code = 400
        else:
           data = {'error': {'code' : code, 'message' : 'Bad request', 'information' : 'Incorrect credentials'}}
           code = 400

    return json.dumps(data), code


def get_key(userid):
    return hashlib.sha224(str(userid) + datetime.utcnow().strftime(DATE_FORMAT)).hexdigest()


def get_expire():
    return datetime.utcnow() + timedelta(days=SESSION_EXPIRE_DAY)


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    key =  request.json.get('key')
    code = 400
    if key is not None:
        sess = Session1.query.filter_by(key=key).first()
        if sess is not None:
            # db.session.delete(sess)
            sess.expire = datetime.utcnow()
            db.session.commit()
            data = {'message': 'ok', 'code': 200}
        else:
            data = {'error' : {'code' : code, 'message' : 'Bad request', 'information' : 'Unrecognized key value'}}
    else:
        data = {'error' : {'code' : code, 'message' : 'Bad request', 'information' : 'Incorrect parameters'}}
        
    return json.dumps(data), code


@app.route('/status', methods=['POST', 'GET'])
def chkuser():
    key = request.json.get('key')
    code = 400
    if key is not None:
        sess = Session1.query.filter_by(key=key).first()
        if sess is not None:
            data = {'userid': sess.user_id}
            code = 200
        else:
            data = {'error' : {'code' : code, 'message' : 'Bad request', 'information' : 'Unrecognized key value'}}
    else:
        data = {'error' : {'code' : code, 'message' : 'Bad request', 'information' : 'Incorrect parameters'}}

    return json.dumps(data), code