from flask import Blueprint, render_template, session, redirect, url_for, request
from database import con
import os
import uuid
from werkzeug.utils import secure_filename
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

# ==========================================
# Add Product
# ==========================================
@product_bp.route("/add_product", methods=["GET", "POST"])
def add_product():

    if "user" not in session:
        return redirect(url_for("auth.login"))

    # ======================================
    # Load Categories
    # ======================================

    res = con.cursor()

    sql = """
    SELECT
        category_id,
        category_name
    FROM category
    ORDER BY category_name
    """

    res.execute(sql)

    categories = fetch_all_dict(res)

    # ======================================
    # Load Suppliers
    # ======================================

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

    # ======================================
    # Save Product
    # ======================================

    if request.method == "POST":

        product_name = request.form["product_name"]
        category_id = request.form["category_id"]
        supplier_id = request.form["supplier_id"]
        price = request.form["price"]
        stock = request.form["stock"]
        description = request.form["description"]

        # Image Upload
        image = request.files["image"]

        filename = "no-image.png"

        if image and image.filename != "":

            extension = os.path.splitext(image.filename)[1]

            filename = str(uuid.uuid4()) + extension

            image.save(
                os.path.join(
                    "static/images",
                    filename
                )
            )

        # ==============================
        # Duplicate Product Check
        # ==============================

        res = con.cursor()

        sql = """
        SELECT *
        FROM product
        WHERE product_name = ?
        """

        res.execute(sql, (product_name,))

        product = fetch_one_dict(res)

        if product:

            return render_template(
                "add_product.html",
                error="Product already exists.",
                product_name=product_name,
                categories=categories,
                suppliers=suppliers
            )

        # ==============================
        # Insert Product
        # ==============================

        res = con.cursor()

        sql = """
        INSERT INTO product
        (
            product_name,
            category_id,
            supplier_id,
            price,
            stock,
            image,
            description
        )
        VALUES
        (?, ?, ?, ?, ?, ?, ?)
        """

        value = (
            product_name,
            category_id,
            supplier_id,
            price,
            stock,
            filename,
            description
        )

        res.execute(sql, value)

        con.commit()

        flash("Product added successfully.", "success")

        return redirect(url_for("product.product"))

    # ======================================
    # Load Page
    # ======================================

    return render_template(
        "add_product.html",
        categories=categories,
        suppliers=suppliers
    )

#==================
# Update prouduct
#==================
@product_bp.route('/update_product/<int:product_id>',methods=['GET','POST'])
def update_product():

    if 'user' not in session:
        return redirect('auth.login')
    
    # ======================================
    # Load Categories
    # ======================================

    res = con.cursor()

    sql = 'select category_id,category_name from category' \
    ' order by category_name'

    res.execute(sql)

    categories = fetch_all_dict(res)

    # ======================================
    # Load Suppliers
    # ======================================
    res = con.cursor()

    sql = 'select supplier_id,supplier_name from suppliers' \
    'order by supplier_name'

    res.execute(sql)

    suppliers = fetch_all_dict(res)

    # ======================================
    # Save Product
    # ======================================




    
