from flask import Flask
from routes.auth import auth_bp

app = Flask(__name__)

app.secret_key = "inventory_management_secret_key"

#Blueprints
app.register_blueprint(auth_bp)

if __name__ == "__main__":

    app.run(debug=True,port=8000)