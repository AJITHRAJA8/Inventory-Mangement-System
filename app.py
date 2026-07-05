from flask import Flask
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.category import category_bp
from routes.supplier import supplier_bp
from routes.product import product_bp
from routes.stock_in import stock_in_bp
from routes.stock_out import stock_out_bp
from routes.customer import customer_bp
from routes.reports import reports_bp

app = Flask(__name__)

app.secret_key = "inventory_management_secret_key"

#Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(category_bp)
app.register_blueprint(supplier_bp)
app.register_blueprint(product_bp)
app.register_blueprint(stock_in_bp)
app.register_blueprint(stock_out_bp)
app.register_blueprint(customer_bp)
app.register_blueprint(reports_bp)

if __name__ == "__main__":

    app.run(debug=True,port=8000)