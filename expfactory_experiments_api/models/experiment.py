from sqlalchemy.ext.hybrid import hybrid_property

from expfactory_experiments_api.extensions import db, pwd_context


class Experiment(db.Model):
    """Basic Experiment Model"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024), unique=True, nullable=False)
    config = db.Column(db.Text(), unique=True, nullable=False)

    def __repr__(self):
        return "<Exp %s>" % self.name
