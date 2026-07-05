from flask import Blueprint, render_template, request, redirect, url_for, session
from database import con
from helpers import fetch_all_dict
import math

customer_bp = Blueprint("customer", __name__)


# ==========================================
# Customer List
# ==========================================

@customer_bp.route('/customer', methods=['GET'])
def customer():

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    search = request.args.get("search", "")

    per_page = 5

    page = request.args.get("page", 1, type=int)

    offset = (page - 1) * per_page

    res = con.cursor()

    # Search
    if search:

        sql = """
        SELECT COUNT(*)

        FROM customer

        WHERE

        customer_name LIKE ?

        OR phone LIKE ?

        OR email LIKE ?
        """

        value = (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        )

        res.execute(sql, value)

        total = res.fetchone()[0]

        sql = """
        SELECT *

        FROM customer

        WHERE

        customer_name LIKE ?

        OR phone LIKE ?

        OR email LIKE ?

        ORDER BY customer_id DESC

        OFFSET ? ROWS

        FETCH NEXT ? ROWS ONLY
        """

        value = (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%",
            offset,
            per_page
        )

        res.execute(sql, value)

    else:

        sql = "SELECT COUNT(*) FROM customer"

        res.execute(sql)

        total = res.fetchone()[0]

        sql = """
        SELECT *

        FROM customer

        ORDER BY customer_id DESC

        OFFSET ? ROWS

        FETCH NEXT ? ROWS ONLY
        """

        res.execute(sql, (offset, per_page))

    datas = fetch_all_dict(res)

    total_pages = math.ceil(total / per_page)

    if total_pages == 0:

        total_pages = 1

    return render_template(

        "customer.html",

        datas=datas,

        search=search,

        current_page=page,

        total_pages=total_pages

    )