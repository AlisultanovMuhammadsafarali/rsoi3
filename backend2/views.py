from backend2 import app
from flask import request, session, g, redirect, url_for, abort, \
                  render_template, flash, make_response, jsonify

from models import db, Entries
db.init_app(app)


@app.route('/entries')
def entries():
    code = 400
    userid = request.json.get('userid')
    if userid is not None:
        u = Entries.query.get(id=userid)
        entry = u.Entries.all()
        if entry is not None:
            code = 200
            data = {'entries': entry}
        else:
            code 204
            data = {'error': {'code': code, 'message': 'No Content'}}
    else:
        data = {'error': {'code': code, 'message': 'Bad request', 'information': 'Incorrect credentials'}}

    return json.dumps(data), code