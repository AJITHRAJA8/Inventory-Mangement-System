from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import con
from helpers import fetch_all_dict, fetch_one_dict
import math

stock_in_bp = Blueprint("stock_in", __name__)


# ==========================================
# Stock In List
# ==========================================
@stock_in_bp.route('/stock_in', methods=['GET'])
def stock_in():

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
        FROM stock_in s
        INNER JOIN product p
            ON s.product_id = p.product_id
        INNER JOIN supplier sp
            ON s.supplier_id = sp.supplier_id
        WHERE
            p.product_name LIKE ?
            OR sp.supplier_name LIKE ?
        """

        value = (
            f"%{search}%",
            f"%{search}%"
        )

        res.execute(sql, value)

        total = res.fetchone()[0]

        sql = """
        SELECT

            s.*,

            p.product_name,

            sp.supplier_name

        FROM stock_in s

        INNER JOIN product p
            ON s.product_id = p.product_id

        INNER JOIN supplier sp
            ON s.supplier_id = sp.supplier_id

        WHERE

            p.product_name LIKE ?

            OR sp.supplier_name LIKE ?

        ORDER BY stockin_id DESC

        OFFSET ? ROWS

        FETCH NEXT ? ROWS ONLY
        """

        value = (
            f"%{search}%",
            f"%{search}%",
            offset,
            per_page
        )

        res.execute(sql, value)

    else:

        sql = """
        SELECT COUNT(*)
        FROM stock_in
        """

        res.execute(sql)

        total = res.fetchone()[0]

        sql = """
        SELECT

            s.*,

            p.product_name,

            sp.supplier_name

        FROM stock_in s

        INNER JOIN product p
            ON s.product_id = p.product_id

        INNER JOIN supplier sp
            ON s.supplier_id = sp.supplier_id

        ORDER BY stockin_id DESC

        OFFSET ? ROWS

        FETCH NEXT ? ROWS ONLY
        """

        res.execute(sql, (offset, per_page))

    datas = fetch_all_dict(res)

    total_pages = math.ceil(total / per_page)

    if total_pages == 0:
        total_pages = 1

    return render_template(
        "stock_in.html",
        datas=datas,
        current_page=page,
        total_pages=total_pages,
        search=search
    )

# ==========================================
# Add Stock In
# ==========================================
@stock_in_bp.route('/add_stock_in', methods=['GET', 'POST'])
def add_stock_in():

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    # -----------------------------
    # Load Products
    # -----------------------------

    res = con.cursor()

    sql = """
    SELECT
        product_id,
        product_name
    FROM product
    ORDER BY product_name
    """

    res.execute(sql)

    products = fetch_all_dict(res)

    # -----------------------------
    # Load Suppliers
    # -----------------------------

    res = con.cursor()

    sql = """
    SELECT
        supplier_id,
        supplier_name
    FROM supplier
    ORDER BY supplier_name
    """

    res.execute(sql)

    suppliers = fetch_all_dict(res)

    # -----------------------------
    # Save Stock In
    # -----------------------------

    if request.method == "POST":

        product_id = request.form["product_id"]

        supplier_id = request.form["supplier_id"]

        quantity = int(request.form["quantity"])

        purchase_price = request.form["purchase_price"]

        stock_in_date = request.form["stock_in_date"]

        remarks = request.form["remarks"]

        # -----------------------------
        # Insert Stock In
        # -----------------------------

        res = con.cursor()

        sql = """
        INSERT INTO stock_in
        (
            product_id,
            supplier_id,
            quantity,
            purchase_price,
            stock_in_date,
            remarks
        )
        VALUES
        (
            ?, ?, ?, ?, ?, ?
        )
        """

        value = (
            product_id,
            supplier_id,
            quantity,
            purchase_price,
            stock_in_date,
            remarks
        )

        res.execute(sql, value)

        # -----------------------------
        # Update Product Stock
        # -----------------------------

        sql = """
        UPDATE product

        SET stock = stock + ?

        WHERE product_id = ?
        """

        res.execute(sql, (quantity, product_id))

        con.commit()

        flash(
            "Stock added successfully.",
            "success"
        )

        return redirect(
            url_for("stock_in.stock_in")
        )

    return render_template(
        "add_stock_in.html",
        products=products,
        suppliers=suppliers
    )