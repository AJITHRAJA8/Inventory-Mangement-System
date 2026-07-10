from flask import Blueprint, render_template, session, redirect, url_for, request,flash
from database import con
import os
import uuid
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

        sql = "EXEC usp_Product_SearchCount ?"

        value = (search ,)

        res.execute(sql, value)

        total = fetch_one_dict(res)["total"]

        total_pages = math.ceil(total / per_page)

        sql = "EXEC usp_Product_SearchPaged ?, ?, ?"

        value = (
            search,
            offset,
            per_page
        )

        res.execute(sql, value)

    # ==========================
    # Normal Product List
    # ==========================

    else:

        sql = "EXEC usp_Product_ListCount"

        res.execute(sql)

        total = fetch_one_dict(res)["total"]

        total_pages = math.ceil(total / per_page)

        sql = "EXEC usp_Product_ListPaged ?, ?"

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

    sql = "EXEC usp_Category_GetDropdown"

    res.execute(sql)

    categories = fetch_all_dict(res)

    # ======================================
    # Load Suppliers
    # ======================================

    res = con.cursor()

    sql = "EXEC usp_Supplier_GetAll"

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

        sql = "EXEC usp_Product_GetByName ?"

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

        sql = 'exec getvalue ?,?,?,?,?,?,?'

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

# ==========================================
# Update Product
# ==========================================
@product_bp.route('/update_product/<int:product_id>', methods=['GET', 'POST'])
def update_product(product_id):

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    # ==========================
    # Load Categories
    # ==========================

    res = con.cursor()

    sql = "EXEC usp_Category_GetDropdown"

    res.execute(sql)

    categories = fetch_all_dict(res)

    # ==========================
    # Load Suppliers
    # ==========================

    res = con.cursor()

    sql = "EXEC usp_Supplier_GetAll"

    res.execute(sql)

    suppliers = fetch_all_dict(res)

    # ==========================
    # Update Product
    # ==========================

    if request.method == "POST":

        product_name = request.form["product_name"]
        category_id = request.form["category_id"]
        supplier_id = request.form["supplier_id"]
        price = request.form["price"]
        stock = request.form["stock"]
        description = request.form["description"]

        # Duplicate Check

        res = con.cursor()

        sql = "EXEC usp_Product_CheckDuplicateForUpdate ?, ?"

        res.execute(sql, (product_name, product_id))

        product = fetch_one_dict(res)

        if product:

            # Load Current Product

            res = con.cursor()

            sql = "EXEC usp_Product_GetById ?"

            res.execute(sql, (product_id,))

            data = fetch_one_dict(res)

            return render_template(
                "update_product.html",
                error="Product already exists.",
                data=data,
                categories=categories,
                suppliers=suppliers
            )

        # ==========================
        # Current Image
        # ==========================

        res = con.cursor()

        sql = "EXEC usp_Product_GetImageById ? "

        res.execute(sql, (product_id,))

        old_image = fetch_one_dict(res)["image"]

        filename = old_image

        image = request.files["image"]

        # ==========================
        # New Image Uploaded
        # ==========================

        if image and image.filename != "":

            extension = os.path.splitext(image.filename)[1]

            filename = str(uuid.uuid4()) + extension

            image.save(
                os.path.join(
                    "static/images",
                    filename
                )
            )

            # Delete Old Image

            if old_image != "no-image.png":

                old_path = os.path.join(
                    "static/images",
                    old_image
                )

                if os.path.exists(old_path):

                    os.remove(old_path)

        # ==========================
        # Update product
        # ==========================

        res = con.cursor()

        sql = "EXEC usp_Product_Update ?, ?, ?, ?, ?, ?, ?, ?"

        value = (
            product_name,
            category_id,
            supplier_id,
            price,
            stock,
            filename,
            description,
            product_id
        )

        res.execute(sql, value)

        con.commit()

        flash("Product updated successfully.", "success")

        return redirect(url_for("product.product"))

    # ==========================
    # Display Product
    # ==========================

    res = con.cursor()

    sql = "EXEC usp_Product_GetById ?"

    res.execute(sql, (product_id,))

    result = fetch_one_dict(res)

    return render_template(
        "update_product.html",
        data=result,
        categories=categories,
        suppliers=suppliers
    )

# ==========================================
# Delete Product
# ==========================================
@product_bp.route('/delete_product/<int:product_id>', methods=['GET', 'POST'])
def delete_product(product_id):

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    if request.method == "POST":

        # Get Current Image

        res = con.cursor()

        sql = "EXEC usp_Product_GetImageById ?"

        res.execute(sql, (product_id,))

        image = fetch_one_dict(res)["image"]

        # Delete Image File

        if image != "no-image.png":

            path = os.path.join(
                "static/images",
                image
            )

            if os.path.exists(path):

                os.remove(path)

        # Delete Product

        res = con.cursor()

        sql = "EXEC usp_Product_Delete ?"

        res.execute(sql, (product_id,))

        con.commit()

        flash("Product deleted successfully.", "success")

        return redirect(url_for("product.product"))

    # ==========================
    # Display Product Details
    # ==========================

    res = con.cursor()

    sql = "EXEC usp_Product_GetDetailsById ?"

    res.execute(sql, (product_id,))

    result = fetch_one_dict(res)

    return render_template(
        "delete_product.html",
        data=result
    )