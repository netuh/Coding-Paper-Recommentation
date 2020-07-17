from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskblog.users.routes import users
    from flaskblog.main.routes import main
    from flaskblog.finder.routes import finder
    from flaskblog.guidelines.routes import guidelines
    from flaskblog.data_vizualization.routes import data_vizualization
    from flaskblog.design.routes import design
    from flaskblog.task.routes import task
    from flaskblog.sampling.routes import sampling
    from flaskblog.measurements.routes import measurements
    from flaskblog.statistics.routes import statistics
    from flaskblog.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(finder)
    app.register_blueprint(guidelines)
    app.register_blueprint(data_vizualization)
    app.register_blueprint(design)
    app.register_blueprint(task)
    app.register_blueprint(sampling)
    app.register_blueprint(measurements)
    app.register_blueprint(statistics)
    app.register_blueprint(errors)

    return app
