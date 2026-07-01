from flask import Blueprint, render_template, session, redirect, url_for

dashboard_db = Blueprint("dashboard", __name__)

@dashboard_db.route("/home")
def home():

    if "user" not in session:
        return redirect(url_for("auth.login"))

    return render_template('home.html')