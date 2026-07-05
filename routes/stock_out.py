from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import con
from helpers import fetch_all_dict, fetch_one_dict
import math

stock_out_bp = Blueprint("stock_out", __name__)

# ==========================================
# Stock Out
# ==========================================

@stock_out_bp.route('/stock_out')
def stock_out():

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    search = request.args.get('search', '')

    per_page = 5

    page = request.args.get('page', 1, type=int)

    offset = (page - 1) * per_page

    res = con.cursor()

    # Total Records

    if search:

        sql = """
        SELECT COUNT(*) total

        FROM stock_out s

        INNER JOIN product p

        ON s.product_id = p.product_id

        WHERE

        p.product_name LIKE ?
        """

        res.execute(sql, ('%' + search + '%',))

    else:

        sql = "SELECT COUNT(*) total FROM stock_out"

        res.execute(sql)

    total_records = res.fetchone()[0]

    total_pages = math.ceil(total_records / per_page)

    # Display Records

    res = con.cursor()

    if search:

        sql = """

        SELECT

        s.stockout_id,

        p.product_name,

        s.quantity,

        s.stockout_date,

        s.remarks

        FROM stock_out s

        INNER JOIN product p

        ON s.product_id = p.product_id

        WHERE

        p.product_name LIKE ?

        ORDER BY s.stockout_id DESC

        OFFSET ? ROWS

        FETCH NEXT ? ROWS ONLY

        """

        res.execute(
            sql,
            (
                '%' + search + '%',
                offset,
                per_page
            )
        )

    else:

        sql = """

        SELECT

        s.stockout_id,

        p.product_name,

        s.quantity,

        s.stockout_date,

        s.remarks

        FROM stock_out s

        INNER JOIN product p

        ON s.product_id = p.product_id

        ORDER BY s.stockout_id DESC

        OFFSET ? ROWS

        FETCH NEXT ? ROWS ONLY

        """

        res.execute(
            sql,
            (
                offset,
                per_page
            )
        )

    datas = fetch_all_dict(res)

    return render_template(

        "stock_out.html",

        datas=datas,

        search=search,

        current_page=page,

        total_pages=total_pages

    )