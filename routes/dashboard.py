from flask import Blueprint, render_template, session, redirect, url_for
from database import con
from helpers import fetch_all_dict, fetch_one_dict

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/home")
def home():

    if "user" not in session:

        return redirect(url_for("auth.login"))

    # -----------------------------------
    # Total Products
    # -----------------------------------

    res = con.cursor()

    sql = "EXEC usp_Product_GetCount"

    res.execute(sql)

    result = fetch_one_dict(res)

    # -----------------------------------
    # In Stock Products
    # -----------------------------------

    res = con.cursor()

    sql = "EXEC usp_Product_GetStockInCount"

    res.execute(sql)

    stock = fetch_one_dict(res)

    # -----------------------------------
    # Low Stock Products
    # -----------------------------------

    res = con.cursor()

    sql = """
    SELECT COUNT(*) AS status
    FROM product
    WHERE stock BETWEEN 1 AND 10
    """

    res.execute(sql)

    low = fetch_one_dict(res)

    # -----------------------------------
    # Out Of Stock Products
    # -----------------------------------

    res = con.cursor()

    sql = """
    SELECT COUNT(*) AS out_stock
    FROM product
    WHERE stock = 0
    """

    res.execute(sql)

    out = fetch_one_dict(res)

    # -----------------------------------
    # Total Suppliers
    # -----------------------------------

    res = con.cursor()

    sql = """
    SELECT COUNT(*) AS total_supplier
    FROM supplier
    """

    res.execute(sql)

    supplier = fetch_one_dict(res)

    # -----------------------------------
    # Recent Stock In
    # -----------------------------------

    res = con.cursor()

    sql = """

    SELECT TOP 3

        p.image,

        p.product_name,

        s.supplier_name,

        si.stockin_date,

        si.quantity

    FROM stock_in si

    INNER JOIN product p

        ON si.product_id = p.product_id

    INNER JOIN supplier s

        ON si.supplier_id = s.supplier_id

    ORDER BY si.stockin_date DESC

    """

    res.execute(sql)

    recent_stockin = fetch_all_dict(res)

    # -----------------------------------
    # Recent Stock Out
    # -----------------------------------

    res = con.cursor()

    sql = """

    SELECT TOP 3

        p.image,

        p.product_name,

        c.customer_name,

        so.stockout_date,

        so.quantity

    FROM stock_out so

    INNER JOIN product p

        ON so.product_id = p.product_id

    INNER JOIN customer c

        ON so.customer_id = c.customer_id

    ORDER BY so.stockout_date DESC

    """

    res.execute(sql)

    recent_stockout = fetch_all_dict(res)

    # -----------------------------------
    # Low Stock Products
    # -----------------------------------

    res = con.cursor()

    sql = """

    SELECT TOP 3

        product_name,

        image,

        stock

    FROM product

    WHERE stock BETWEEN 1 AND 10

    ORDER BY stock ASC

    """

    res.execute(sql)

    low_stock_products = fetch_all_dict(res)

    return render_template(

        "home.html",

        datas=result,

        stock=stock,

        low=low,

        out=out,

        supplier=supplier,

        recent_stockin=recent_stockin,

        recent_stockout=recent_stockout,

        low_stock_products=low_stock_products

    )

