import json

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from expfactory_experiments_api.api.schemas import ExperimentSchema, ExperimentListSchema
from expfactory_experiments_api.models import Experiment
from expfactory_experiments_api.extensions import db
from expfactory_experiments_api.commons.pagination import paginate


class ExperimentResource(Resource):
    def get(self, name):
        schema = ExperimentSchema()
        exp = Experiment.query.filter_by(name=name).first()
        return json.loads(schema.dump(exp)["config"])

class ExperimentList(Resource):
    def get(self):
        search = request.args.get('search')
        schema = ExperimentListSchema(many=True)
        query = Experiment.query
        if search:
            print(search)
            query = Experiment.query.filter(Experiment.config.ilike(f"%{search}%"))
        return paginate(query, schema)
