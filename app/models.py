from typing import Union, List, Dict

from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    problems = db.relationship('Problem', backref='user', lazy=True)

    def __repr__(self):
        return f'<User(name={self.name})'


class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    problem_number = db.Column(db.Integer)
    solved = db.Column(db.Boolean)
    completed_on = db.Column(db.DateTime)
    correct_answer = db.Column(db.Text)  # not sure if answer can be int/float/etc

    code = db.relationship('Code', backref='problem', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Problem(id={self.id}, user_id={self.user_id})>'


class Code(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(50))
    filecontent = db.Column(db.Text)
    filename = db.Column(db.String(50))
    submission = db.Column(db.String)  # this will mirror the type of the correct answer
    problem_id = db.Column(db.Integer, db.ForeignKey('problem.id'), nullable=False)

    def __repr__(self):
        return f'<Code(problem_id={self.problem_id}, language={self.language})>'


def to_dict(problem) -> Union[List, Dict]:
    code = {}
    for c in problem.code:
        code.update(
            {c.language: {'filecontent': c.filecontent,
                          'filename': c.filename,
                          'submission': c.submission}})
    return {
        'ID': problem.id,
        'Solved': problem.solved,
        'completed_on': problem.completed_on,
        'correct_answer': problem.correct_answer,
        'code': code
    }
