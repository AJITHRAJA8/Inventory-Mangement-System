from flask import Flask
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.category import category_bp
from routes.supplier import supplier_bp
from routes.product import product_bp

app = Flask(__name__)

app.secret_key = "inventory_management_secret_key"

#Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(category_bp)
app.register_blueprint(supplier_bp)
app.register_blueprint(product_bp)

if __name__ == "__main__":

    app.run(debug=True,port=8000)