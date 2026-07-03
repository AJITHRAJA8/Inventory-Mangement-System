from flask import Blueprint, render_template, session, redirect, url_for
from database import con
from helpers import fetch_all_dict, fetch_one_dict

supplier_bp = Blueprint("supplier", __name__)

#supplier route
@supplier_bp.route('/supplier',methods=['GET','POST'])
def supplier():

    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    res = con.cursor()
    sql = 'select * from supplier order by supplier_id '
    res.execute(sql)
    result = fetch_all_dict(res)
    return render_template('supplier.html',datas=result)