from flask import Flask

app = Flask(__name__)

app.secret_key = "Top Secret "
from flask_app.controllers.main import motors_bp
app.register_blueprint(motors_bp)