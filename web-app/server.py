from flask_app import app

from flask_app.controllers import main

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)