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

        c.customer_name,

        p.product_name,

        s.quantity,

        s.stockout_date,

        s.remarks

        FROM stock_out s

        INNER JOIN product p

        ON s.product_id = p.product_id

        INNER JOIN CUSTOMER C

        ON c.customer_id = s.customer_id

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

        c.customer_name,

        p.product_name,

        s.quantity,

        s.stockout_date,

        s.remarks

        FROM stock_out s

        INNER JOIN product p

        ON s.product_id = p.product_id

        INNER JOIN CUSTOMER C

        ON c.customer_id = s.customer_id

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

# ==========================================
# Add Stock Out
# ==========================================

@stock_out_bp.route('/add_stock_out', methods=['GET', 'POST'])
def add_stock_out():

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    # -----------------------------
    # Customer Dropdown
    # -----------------------------

    res = con.cursor()

    sql = """
    SELECT

    customer_id,

    customer_name

    FROM customer

    ORDER BY customer_name
    """

    res.execute(sql)

    customers = fetch_all_dict(res)

    # -----------------------------
    # Product Dropdown
    # -----------------------------

    res = con.cursor()

    sql = """
    SELECT

    product_id,

    product_name,

    stock

    FROM product

    ORDER BY product_name
    """

    res.execute(sql)

    products = fetch_all_dict(res)

    if request.method == "POST":

        customer_id = request.form["customer_id"]

        product_id = request.form["product_id"]

        quantity = int(request.form["quantity"])

        stockout_date = request.form["stockout_date"]

        remarks = request.form["remarks"]

        # -----------------------------
        # Check Available Stock
        # -----------------------------

        res = con.cursor()

        sql = """
        SELECT

        stock

        FROM product

        WHERE product_id = ?
        """

        res.execute(sql, (product_id,))

        product = fetch_one_dict(res)

        current_stock = product["stock"]

        # -----------------------------
        # Validation
        # -----------------------------

        if quantity > current_stock:

            return render_template(

                "add_stock_out.html",

                customers=customers,

                products=products,

                error=f"Insufficient stock. Available Stock : {current_stock}",

                data={

                    "customer_id": customer_id,

                    "product_id": product_id,

                    "quantity": quantity,

                    "stockout_date": stockout_date,

                    "remarks": remarks

                }

            )

        # -----------------------------
        # Insert Stock Out
        # -----------------------------

        res = con.cursor()

        sql = """
        INSERT INTO stock_out
        (
            product_id,
            customer_id,
            quantity,
            stockout_date,
            remarks
        )

        VALUES
        (
            ?, ?, ?, ?, ?
        )
        """

        value = (

            product_id,

            customer_id,

            quantity,

            stockout_date,

            remarks

        )

        res.execute(sql, value)

        # -----------------------------
        # Reduce Product Stock
        # -----------------------------

        sql = """
        UPDATE product

        SET stock = stock - ?

        WHERE product_id = ?
        """

        res.execute(

            sql,

            (

                quantity,

                product_id

            )

        )

        con.commit()

        flash(

            "Stock Out recorded successfully.",

            "success"

        )

        return redirect(

            url_for("stock_out.stock_out")

        )

    return render_template(

        "add_stock_out.html",

        customers=customers,

        products=products

    )