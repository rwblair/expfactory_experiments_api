import click
import git
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

def get_experiment_type(experiment):
    if experiment["template"] in ["jspsych"]:
        return "experiments"
    elif experiment["template"] in ["survey"]:
        return "surveys"
    elif experiment["template"] in ["phaser"]:
        return "games"

exclude = ["run"]

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
            config_json = json.load(fp)[0]
            name = config_json["exp_id"]
            exp_in_db = db.session.query(Experiment).filter_by(name=name).first()
            if exp_in_db is None:
                config_json["preview"] = f"https://expfactory.org/{name}/preview"
                repo = git.Repo(root, search_parent_directories=True)
                repo_path = repo.git.rev_parse("--show-toplevel")
                config_json["type"] = get_experiment_type(config_json)
                origin = repo.remotes.origin.url
                if origin.endswith('.git'):
                    origin = origin[:-4]
                config_json["origin"] = origin
                config_json["version"] = f"{origin}/commit/{repo.head.commit.hexsha}"
                [config_json.pop(x) for x in exclude]
                exp = Experiment(name=name, config=json.dumps(config_json))
                db.session.add(exp)
                db.session.commit()


if __name__ == "__main__":
    cli()
