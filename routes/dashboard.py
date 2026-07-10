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

    sql = "EXEC usp_Product_GetLowStockCount"

    res.execute(sql)

    low = fetch_one_dict(res)

    # -----------------------------------
    # Out Of Stock Products
    # -----------------------------------

    res = con.cursor()

    sql = "EXEC usp_Product_GetOutOfStockCount"

    res.execute(sql)

    out = fetch_one_dict(res)

    # -----------------------------------
    # Total Suppliers
    # -----------------------------------

    res = con.cursor()

    sql = "EXEC usp_Supplier_GetCount"

    res.execute(sql)

    supplier = fetch_one_dict(res)

    # -----------------------------------
    # Recent Stock In
    # -----------------------------------

    res = con.cursor()

    sql = "EXEC usp_StockIn_GetRecent"

    res.execute(sql)

    recent_stockin = fetch_all_dict(res)

    # -----------------------------------
    # Recent Stock Out
    # -----------------------------------

    res = con.cursor()

    sql = "EXEC usp_StockOut_GetRecent"

    res.execute(sql)

    recent_stockout = fetch_all_dict(res)

    # -----------------------------------
    # Low Stock Products
    # -----------------------------------

    res = con.cursor()

    sql = "EXEC usp_Product_GetLowStockList"

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

