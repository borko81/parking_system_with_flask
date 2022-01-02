from decouple import config
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from db import db
from resources.routers import routers


class DevelopmentConfig:
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://rcicpassleifnf:8a1985ba34eb598459a0d2bf39bef1ad35be401175ca7e9dff53e86cbd477fd7@ec2-63-32-7-190.eu-west-1.compute.amazonaws.com:5432/demp4j96vm74a2'


class ProductionConfig:
    FLASK_ENV = "prod"
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://rcicpassleifnf:8a1985ba34eb598459a0d2bf39bef1ad35be401175ca7e9dff53e86cbd477fd7@ec2-63-32-7-190.eu-west-1.compute.amazonaws.com:5432/demp4j96vm74a2'


class TestingConfig:
    FLASK_ENV = "testing"
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}"
        f"@localhost:{config('DB_PORT')}/{config('DB_TEST_NAME')}"
    )


def create_app(config="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config)

    api = Api(app)
    migrate = Migrate(app, db)
    [api.add_resource(*route) for route in routers]
    return app
