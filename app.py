from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from sqlalchemy import exc
from werkzeug.exceptions import BadRequest

from db import db
from resources.routers import routers

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

api = Api(app)
migrate = Migrate(app, db, compare_type=True)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.init_app(app)
    db.create_all()


@app.after_request
def close_request(response):
    db.session.commit()
    return response

@app.errorhandler(exc.SQLAlchemyError)
def handle_db_exceptions(error):
    #log the error: app.logger.error(error)
    db.session.rollback()
    raise BadRequest(error)


@app.route("/test_is_alive")
def test_is_alive():
    return {"message": "Server still alive"}


[api.add_resource(*route) for route in routers]

if __name__ == "__main__":
    app.run()
