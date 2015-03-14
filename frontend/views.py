from frontend import app
from flask import request, session, g, redirect, url_for, abort, \
                  render_template, flash, make_response, jsonify
import json, requests

headers={'Content-Type': 'application/json'}


@app.route('/')
@app.route('/index')
def index():
    key = request.cookies.get('key')
    response = redirect('/login')
    if key is not None:
        body = json.dumps({'key': key})
        res = requests.post('http://localhost:5003/status', data=body, headers=headers)
        if res.status_code == 200:
            response = redirect('/entries')

    return response


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        body = json.dumps({'username': request.form['username'], 'password': request.form['password']})
        res = requests.get('http://localhost:5003/login', data=body, headers=headers)
        if res.status_code == 200:
            data = json.loads(res.text)
            response = redirect('/entries')
            response.set_cookie('key', value=data['key'])

            return response

    return render_template('login.html', access=False)


@app.route('/logout')
def logout():
    response = make_response(render_template('login.html', access=False))
    response.delete_cookie('key')
    return response


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


@app.route('/entries', methods=['POST', 'GET'])
def entries():
    if request.method == 'GET':
        key = request.cookies.get('key')
        if key is not None:
            body = json.dumps({'key': key})
            res = requests.post('http://localhost:5003/status', data=body, headers=headers)
            if res.status_code == 200:
                data = json.loads(res.text)
                body = json.dumps(data)
                res_b2 = requests.get('http://localhost:5002/entries', data=body, headers=headers)

                data = json.loads(res_b2.text)
                return render_template('entries.html', access=True, entries=data)
            else:
                flash(json.loads(res.text)['error'])
        else:
            return redirect('/logout')

    return render_template('entries.html', access=True)


@app.route('/entries/add', methods=['POST'])
def addentries():
    if request.method == 'POST':
        key = request.cookies.get('key')
        if key is not None:
            body = json.dumps({'key': key})
            res = requests.post('http://localhost:5003/status', data=body, headers=headers)
            if res.status_code == 200:
                title = request.form['title']
                text = request.form['text']
                data = {'entry': {'userid': json.loads(res.text)['userid'], 'title': title, 'text': text}}
                body = json.dumps(data)
                res_b2 = requests.post('http://localhost:5002/entries/add', data=body, headers=headers)
                if res_b2.status_code == 200:
                    flash('New entry was successfully posted')
                else:
                    flash('failed add new entry')

                return redirect('/entries')
            else:
                flash(json.loads(res.text)['error'])
                return redirect('/entries')
        else:
            return redirect('/logout')

    return render_template('entries.html')


@app.route('/entries/allusers')
def all():
    key = request.cookies.get('key')
    if key is not None:
        body = json.dumps({'key': key})
        res = requests.post('http://localhost:5003/status', data=body, headers=headers)
        if res.status_code == 200:
            data = json.loads(res.text)
            body = json.dumps(data)
            res_b1 = requests.get('http://localhost:5001/me', data=body, headers=headers)
            data = json.loads(res_b1.text)
            return jsonify({'res_b1': res_b1.text})
            if res_b1.status_code == 200:
                datame = json.loads(res_b1.text)
                return jsonify({'data': datame})

    else:
        return redirect('/logout')

    return redirect('/entries')