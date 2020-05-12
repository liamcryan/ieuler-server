import json
import os

from flask import Flask, request, jsonify, current_app
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
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'interactive-project-euler.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    from .models import db, Problem, Code, to_dict, User
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
        if current_app.config['TESTING']:
            return True

        try:  # try to convert to dict
            cookies = json.loads(cookies)
        except (json.decoder.JSONDecodeError,):
            pass

        if not isinstance(cookies, dict):
            return False

        client = Client()
        if client.logged_in(username, cookies):
            return True

    @app.route('/', methods=['POST', 'GET'])
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

        username = auth.current_user()
        _user = User.query.filter_by(name=username).first()
        if not _user:
            _user = User(name=username)

        db.session.add(_user)

        for d in data:
            _problem = User.query.filter_by(name=username).join(Problem).filter_by(problem_number=int(d['ID'])).first()
            if not _problem:
                _problem = Problem()
            _problem.problem_number = int(d['ID'])
            _problem.solved = d.get('Solved')
            _problem.completed_on = d.get('completed_on')
            _problem.correct_answer = d.get('correct_answer')
            _problem.user_id = _user.id

            db.session.add(_problem)

            for k in d.get('code', []):
                _code = User.query.filter_by(name=username).join(Problem).filter_by(problem_number=int(d['ID'])).join(Code).filter_by(language=k).first()
                if not _code:
                    _code = Code()
                _code.language = k
                _code.filecontent = d['code'][k]['filecontent']
                _code.filename = d['code'][k]['filename']
                _code.submission = d['code'][k]['submission']
                _code.problem_id = _problem.id

                db.session.add(_code)

        db.session.commit()

        return jsonify(data), 200

    with app.app_context():
        db.create_all()

        return app
