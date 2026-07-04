from flask import Blueprint, render_template, session, redirect, url_for, request
from database import con
from helpers import fetch_all_dict, fetch_one_dict
import math

product_bp = Blueprint("product", __name__)


# ==========================================
# Product List + Search + Pagination
# ==========================================
@product_bp.route("/product")
def product():

    if "user" not in session:
        return redirect(url_for("auth.login"))

    search = request.args.get("search")

    # Pagination
    per_page = 5
    page = request.args.get("page", 1, type=int)
    offset = (page - 1) * per_page

    res = con.cursor()

    # ==========================
    # Search
    # ==========================

    if search:

        sql = """
        SELECT COUNT(*) AS total
        FROM product
        WHERE product_name LIKE ?
        """

        value = ('%' + search + '%',)

        res.execute(sql, value)

        total = fetch_one_dict(res)["total"]

        total_pages = math.ceil(total / per_page)

        sql = """
        SELECT

            p.product_id,
            p.product_name,
            c.category_name,
            s.supplier_name,
            p.price,
            p.stock,
            p.image

        FROM product p

        INNER JOIN category c
            ON p.category_id = c.category_id

        INNER JOIN supplier s
            ON p.supplier_id = s.supplier_id

        WHERE p.product_name LIKE ?

        ORDER BY p.product_id

        OFFSET ? ROWS
        FETCH NEXT ? ROWS ONLY
        """

        value = (
            '%' + search + '%',
            offset,
            per_page
        )

        res.execute(sql, value)

    # ==========================
    # Normal Product List
    # ==========================

    else:

        sql = """
        SELECT COUNT(*) AS total
        FROM product
        """

        res.execute(sql)

        total = fetch_one_dict(res)["total"]

        total_pages = math.ceil(total / per_page)

        sql = """
        SELECT

            p.product_id,
            p.product_name,
            c.category_name,
            s.supplier_name,
            p.price,
            p.stock,
            p.image

        FROM product p

        INNER JOIN category c
            ON p.category_id = c.category_id

        INNER JOIN supplier s
            ON p.supplier_id = s.supplier_id

        ORDER BY p.product_id

        OFFSET ? ROWS
        FETCH NEXT ? ROWS ONLY
        """

        value = (
            offset,
            per_page
        )

        res.execute(sql, value)

    result = fetch_all_dict(res)

    return render_template(
        "product.html",
        datas=result,
        current_page=page,
        total_pages=total_pages,
        search=search
    )