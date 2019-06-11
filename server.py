
from flask import Flask
app = Flask(__name__)
app.secret_key = "this-is-my-secret-key"

from blueprints.auth import auth
app.register_blueprint(auth)

from blueprints.merc import merc
app.register_blueprint(merc)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
