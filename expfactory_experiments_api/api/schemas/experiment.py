import json
from marshmallow import post_dump
from expfactory_experiments_api.models import Experiment
from expfactory_experiments_api.extensions import ma, db


class ExperimentSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    name = ma.String(dump_only=True, required=True)
    config = ma.String(dump_onlu=True, required=True)

    class Meta:
        model = Experiment
        sqla_session = db.session
        load_instance = True

class ExperimentListSchema(ExperimentSchema):
    @post_dump()  
    def dump_json(self, data, **kwargs):
        return json.loads(data["config"])
