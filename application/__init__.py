from flask import Flask


def init_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.DevConfig')

    with app.app_context():
        # Include our Routes
        from . import routes
        return app
