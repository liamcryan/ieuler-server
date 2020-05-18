from app.models import Problem, User


def test_get_empty(client):
    rv = client.get('/api/problems')
    assert rv.json == []


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
