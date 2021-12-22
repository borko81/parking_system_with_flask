import json

from flasgger import Swagger
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from sqlalchemy import exc
from werkzeug.exceptions import BadRequest

from db import db
from helpers.loger_config import custom_logger
from resources.routers import routers
from config import create_app


app = create_app()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


api = Api(app)
migrate = Migrate(app, db, compare_type=True)
db.init_app(app)
swagger = Swagger(app)


@app.before_first_request
def create_tables():
    db.init_app(app)
    db.create_all()


@app.before_first_request
def create_tables():
    db.init_app(app)
    db.create_all()


@app.after_request
def close_request(response):
    db.session.commit()
    try:
        if response.status_code in [400, 401, 404, 403]:
            custom_logger("error", json.loads(response.data.decode("utf-8")))
    except Exception:
        pass
    return response


@app.errorhandler(exc.SQLAlchemyError)
def handle_db_exceptions(error):
    db.session.rollback()
    custom_logger("error", error)
    raise BadRequest(error)


@app.route("/test_is_alive")
def test_is_alive():
    return {"message": "Server still alive"}


if __name__ == "__main__":
    app.run()
