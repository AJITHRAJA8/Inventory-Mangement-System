from flask import Blueprint, render_template, session, redirect, url_for

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/home")
def home():

    if "user" not in session:
        return redirect(url_for("auth.login"))

    return render_template('home.html')