from flask import Flask

from config import Config
from database import db
from routes import main

def create_app():

    app = Flask(__name__)
    app.register_blueprint(main)

    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)