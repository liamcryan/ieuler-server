from app.models import Problem, User


def test_get_empty(client):
    rv = client.get('/')
    assert rv.json == []


def test_post(client, problems, app):
    rv = client.post('/', json=problems)
    assert rv.json == {}

    with app.app_context():
        _user = User.query.first()
        assert _user.name == None

        _problems = Problem.query.all()
        assert len(_problems) == len(problems)
        for i, j in zip(_problems, problems):
            assert i.id == j['ID']
            assert i.code == []
