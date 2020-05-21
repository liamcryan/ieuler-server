import json
from app.models import Problem, User


def test_get_empty(client):
    rv = client.get('/api/problems')
    assert rv.json == []


def test_get_user_data(client):
    client.post('/api/problems', json=[{"ID": 2, "Description / Title": "Even Fibonacci numbers", "Solved By": "750055",
                                        "problem_url": "https://projecteuler.net/problem=2",
                                        "page_url": "https://projecteuler.net/archives",
                                        "code": {"python3": {"filename": "2.py", "filecontent": "asdf",
                                                             "submission": None}}}])
    r = client.get('/api/problems')
    assert r.json == [{"ID": 2, "Solved": None, "completed_on": None, "correct_answer": None,
                       "code": {"python3": {"filename": "2.py", "filecontent": "asdf", "submission": None}}}]


def test_post(client, problems, app):
    client.post('/api/problems', json=problems)

    with app.app_context():
        _user = User.query.first()
        assert _user.name == None

        _problems = Problem.query.all()
        assert len(_problems) == len(problems)
        for i, j in zip(_problems, problems):
            assert i.id == j['ID']
            assert i.code == []

# todo
#  test badly formatted cookies
#  test wrong username/cookies
