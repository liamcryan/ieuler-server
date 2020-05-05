from app.models import Problem


def test_get_empty(client):
    rv = client.get('/problems')
    assert rv.json == []


def test_post(client, problems, app):
    rv = client.post('/problems', json=problems)
    assert rv.json == {}

    with app.app_context():
        _problems = Problem.query.all()
        for i, j in zip(_problems, problems):
            assert i.id == j['ID']
