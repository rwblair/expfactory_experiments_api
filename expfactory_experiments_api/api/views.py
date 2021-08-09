from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from expfactory_experiments_api.extensions import apispec
from expfactory_experiments_api.api.resources import ExperimentResource, ExperimentList
from expfactory_experiments_api.api.schemas import ExperimentSchema


blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)


api.add_resource(ExperimentResource, "/experiments/<string:name>", endpoint="experiment_by_name")
api.add_resource(ExperimentList, "/experiments", endpoint="experiments")


@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("ExperimentSchema", schema=ExperimentSchema)
    apispec.spec.path(view=ExperimentResource, app=current_app)
    apispec.spec.path(view=ExperimentList, app=current_app)


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400
