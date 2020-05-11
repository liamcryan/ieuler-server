import os

from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from ieuler.client import Client

db = SQLAlchemy()
auth = HTTPBasicAuth()


def create_app(test_config=None):
    # create and configure the app

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'ieuler.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    from .models import db, Problem, Code, to_dict
    db.init_app(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @auth.verify_password
    def verify_user(username, cookies):
        client = Client()
        if client.logged_in(username, cookies):
            return True

    @app.route('/problems', methods=['POST', 'GET'])
    @auth.login_required()
    def problems():
        if request.method == 'GET':
            _response = []
            for p in Problem.query.all():
                _response.append(to_dict(p))
            return jsonify(_response), 200

        # POST
        data = request.json
        if not isinstance(data, list):
            data = [data]
        for d in data:
            _problem = Problem.query.filter_by(id=int(d['ID'])).first()
            if not _problem:
                _problem = Problem()
            _problem.id = int(d['ID'])
            _problem.solved = d.get('Solved')
            _problem.completed_on = d.get('completed_on')
            _problem.correct_answer = d.get('correct_answer')

            for k in d.get('code', []):
                _code = Code(**{'language': k,
                                'filecontent': d['code'][k]['filecontent'],
                                'filename': d['code'][k]['filename'],
                                'submission': d['code'][k]['submission']})
                _problem.code.append(_code)

            db.session.add(_problem)

        db.session.commit()

        return jsonify({}), 200

    with app.app_context():
        db.create_all()

        return app
