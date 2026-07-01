from flask import Blueprint, render_template, session, redirect, url_for
from database import con
from helpers import fetch_all_dict,fetch_one_dict

category_bp = Blueprint('category',__name__)

@category_bp.route('/category',methods=['GET','POST'])
def category():

    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    res=con.cursor()
    sql="SELECT * FROM category order by category_id"
    res.execute(sql)
    result=fetch_all_dict(res)
    return render_template('category.html',datas=result)

