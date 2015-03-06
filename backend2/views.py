from backend2 import app
from flask import request, session, g, redirect, url_for, abort, \
                  render_template, flash, make_response, jsonify

from models import db, Entries
db.init_app(app)


@app.route('/')
@app.route('/index')
def index():
    return jsonify({"message": "backend2"})


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(nickname=request.form['username'])
        return jsonify({"username": user.nickname})
        if user is not None:
            if user.password ==  request.form['password']:
                session['id'] = user.id
                session['logged_in'] = True

                return redirect('me')
            else:
                return make_response(jsonify({"message": "invilid password"}), 401)
        else:
            return make_response(jsonify({"message": "invilid nickname"}), 401)

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


@app.route('/me')
def me():
    if session['logged_in']:
        user = User.query.filter_by(session['id'])
        return render_template('index.html', user=user)

    return make_response(jsonify({"message": "access denied"}), 401)