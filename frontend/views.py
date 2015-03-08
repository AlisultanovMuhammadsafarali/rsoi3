from frontend import app
from flask import request, session, g, redirect, url_for, abort, \
                  render_template, flash, make_response, jsonify
import json, requests

headers={'Content-Type': 'application/json'}


@app.route('/')
@app.route('/index')
def index():
    return render_template('entries.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        body = json.dumps({'username': request.form['username'], 'password': request.form['password']})
        res = requests.post('http://localhost:5003/login', data=body, headers=headers)
        if res.status_code == 200:
            data = json.loads(res.text)
            response = redirect('/entries')
            response.set_cookie('key', value=data['key'])

            return response

    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        nickname = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        phone= request.form.get('phone')
        user = User(nickname, password, email, phone)

        db.session.add(user)
        db.session.commit()

        # user = User.query.filter_by(id=1).first()
        # if user is not None:
        #     data = {'username': user.nickname, 'email': user.email, 'phone': user.phone, "password": user.password}


        # data = {'username' : username,
        #     'password' : password,
        #     'name' : name,
        #     'email' : email,
        #     'tel' : tel}

    #     headers = {'Content-Type' : 'application/json'}
    #     r = requests.post('http://localhost:5002/signup', data=json.dumps(data), headers=headers)
    #     if r.status_code == 200:
    #         response = make_response(render_template('home.html'), r.status_code)
    #     else:
    #         response = make_response(render_template('register.html'), r.status_code)
    # else:
    #     response = make_response(render_template('register.html'))
        return jsonify({"data": data})
    return render_template('signup.html')


@app.route('/entries')
def entries():
    if request.method == 'GET':
        key = request.cookies.get('key')
        if key is not None:
            body = json.dumps({'key': key})
            res = requests.post('http://localhost:5003/status', data=body, headers=headers)
            if res.status_code == 200:
                userid = res.json()['userid']
                data = {'userid': userid}
                resb2 = requests.post('http://localhost:5002/entries', data=data, headers)


    return render_template('entries.html')


@app.route('/me')
def me():
    if session['logged_in']:
        user = User.query.filter_by(session['id'])
        return render_template('index.html', user=user)

    return make_response(jsonify({"message": "access denied"}), 401)