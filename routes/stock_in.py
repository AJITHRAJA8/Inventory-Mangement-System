from flask import Blueprint,request,url_for,flash,redirect,session,render_template
from database import con
from helpers import fetch_all_dict,fetch_one_dict
import math

stock_in_bp = Blueprint('stock_in',__name__)

#View Stocks
@stock_in_bp.route('/stock_in')
def stock_in():

    if 'user' not in session:
        return redirect (url_for('auth.login'))
    
    return render_template("stock_in.html")
