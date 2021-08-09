import click
from flask.cli import with_appcontext


@click.group()
def cli():
    """Main entry point"""


@cli.command("init")
@with_appcontext
def init():
    """Create a new admin user"""
    from expfactory_experiments_api.extensions import db
    from expfactory_experiments_api.models import User

    click.echo("create user")
    user = User(username="admin", email="admin@mail.com", password="admin", active=True)
    db.session.add(user)
    db.session.commit()
    click.echo("created user admin")

@cli.command("import")
@with_appcontext
def import_exps():
    from expfactory_experiments_api.extensions import db
    from expfactory_experiments_api.models import Experiment
    import json
    import os

    valid_dirs = []
    for root, dir, files in os.walk("/experiment_repos"):
        if "config.json" not in files:
            continue
        config_json = None
        with open(os.path.join(root, "config.json")) as fp:
            config_json = json.load(fp)
            exp_in_db = db.session.query(Experiment).filter_by(name=config_json[0]["exp_id"]).first()
            if exp_in_db is None:
                exp = Experiment(name=config_json[0]["exp_id"], config=json.dumps(config_json[0]))
                db.session.add(exp)
                db.session.commit()

if __name__ == "__main__":
    cli()
