from flask import Blueprint, render_template, session, redirect, url_for
from helpers import fetch_one_dict,fetch_all_dict
from database import con

reports_bp = Blueprint(

    "reports",

    __name__

)

# ==========================================
# Reports Dashboard
# ==========================================

@reports_bp.route("/reports")

def reports():

    if "user" not in session:

        return redirect(

            url_for("auth.login")

        )

    return render_template(

        "reports.html"

    )


# ==========================================
# Product Report
# ==========================================

@reports_bp.route("/product_report")
def product_report():

    if "user" not in session:

        return redirect(

            url_for("auth.login")

        )

    res = con.cursor()

    sql = """

    SELECT

    p.product_id,

    p.product_name,

    c.category_name,

    s.supplier_name,

    p.price,

    p.stock

    FROM product p

    INNER JOIN category c

    ON p.category_id = c.category_id

    INNER JOIN supplier s

    ON p.supplier_id = s.supplier_id

    ORDER BY p.product_name

    """

    res.execute(sql)

    datas = fetch_all_dict(res)

    return render_template(

        "product_report.html",

        datas=datas

    )