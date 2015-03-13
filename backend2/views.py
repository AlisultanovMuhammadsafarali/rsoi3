from backend2 import app
from flask import request, session, g, redirect, url_for, abort, \
                  render_template, flash, make_response, jsonify
from sqlalchemy import desc
import json

from models import db, Entries
db.init_app(app)


@app.route('/entries', methods=['POST', 'GET'])
def entries():
    code=400
    userid = request.json.get('userid')
    if userid is not None:
        entry = Entries.query.filter_by(user_fk=userid).all() #order_by(desc(Entries.entry_id))
        # entry = db.session.query(Entries).order_by(Entries.entry_id.desc())

        if entry is not None:
            u = []
            l = len(entry)
            for e in entry[0:l]:
                u.append({'title': e.title, 'text': e.text})

            code = 200
            data = u
            print "in b2 data", data
        else:
            code=204
            data = {'error': {'code': code, 'message': 'No Content'}}
    else:
        data = {'error': {'code': code, 'message': 'Bad request', 'information': 'Incorrect credentials'}}

    return json.dumps(data), code