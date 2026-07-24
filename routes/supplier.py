from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from database import con
from helpers import fetch_all_dict, fetch_one_dict
import math

supplier_bp = Blueprint("supplier", __name__)


# ==========================================
# Supplier List + Search + Pagination
# ==========================================
@supplier_bp.route('/supplier')
def supplier():

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    search = request.args.get("search")

    # Pagination
    per_page = 5

    page = request.args.get("page", 1, type=int)

    offset = (page - 1) * per_page

    res = con.cursor()

    # ===============================
    # Search
    # ===============================

    if search:

        sql = """
        SELECT COUNT(*) AS total
        FROM supplier
        WHERE supplier_name LIKE ?
        """

        value = ('%' + search + '%',)

        res.execute(sql, value)

        total = fetch_one_dict(res)["total"]

        total_pages = math.ceil(total / per_page)

        sql = """
        SELECT *
        FROM supplier
        WHERE supplier_name LIKE ?
        ORDER BY supplier_id
        OFFSET ? ROWS
        FETCH NEXT ? ROWS ONLY
        """

        value = (
            '%' + search + '%',
            offset,
            per_page
        )

        res.execute(sql, value)

    # ===============================
    # Normal List
    # ===============================

    else:

        sql = """
        SELECT COUNT(*) AS total
        FROM supplier
        """

        res.execute(sql)

        total = fetch_one_dict(res)["total"]

        total_pages = math.ceil(total / per_page)

        sql = """
        SELECT *
        FROM supplier
        ORDER BY supplier_id
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
        "supplier.html",
        datas=result,
        current_page=page,
        total_pages=total_pages,
        search=search
    )


# ==========================================
# Add Supplier
# ==========================================
@supplier_bp.route('/add_supplier', methods=['GET', 'POST'])
def add_supplier():

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':

        supplier_name = request.form['supplier_name']
        company_name = request.form['company_name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']

        # Duplicate Check

        res = con.cursor()

        sql = """
        SELECT *
        FROM supplier
        WHERE supplier_name = ?
        """

        res.execute(sql, (supplier_name,))

        supplier = fetch_one_dict(res)

        if supplier:

            return render_template(
                "add_supplier.html",
                error="Supplier already exists.",
                supplier_name=supplier_name,
                company_name=company_name,
                phone=phone,
                email=email,
                address=address
            )

        sql = """
        INSERT INTO supplier
        (
            supplier_name,
            company_name,
            phone,
            email,
            address
        )
        VALUES
        (?, ?, ?, ?, ?)
        """

        value = (
            supplier_name,
            company_name,
            phone,
            email,
            address
        )

        res.execute(sql, value)

        con.commit()

        flash("Supplier added successfully.", "success")

        return redirect(url_for("supplier.supplier"))

    return render_template("add_supplier.html")


# ==========================================
# Update Supplier
# ==========================================
@supplier_bp.route('/update_supplier/<int:supplier_id>', methods=['GET', 'POST'])
def update_supplier(supplier_id):

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':

        supplier_name = request.form['supplier_name']
        company_name = request.form['company_name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']

        # Duplicate Check

        res = con.cursor()

        sql = """
        SELECT *
        FROM supplier
        WHERE supplier_name = ?
        AND supplier_id <> ?
        """

        value = (
            supplier_name,
            supplier_id
        )

        res.execute(sql, value)

        supplier = fetch_one_dict(res)

        if supplier:

            return render_template(
                "update_supplier.html",
                error="Supplier already exists.",
                data={
                    "supplier_id": supplier_id,
                    "supplier_name": supplier_name,
                    "company_name": company_name,
                    "phone": phone,
                    "email": email,
                    "address": address
                }
            )

        sql = """
        UPDATE supplier
        SET
            supplier_name = ?,
            company_name = ?,
            phone = ?,
            email = ?,
            address = ?
        WHERE supplier_id = ?
        """

        value = (
            supplier_name,
            company_name,
            phone,
            email,
            address,
            supplier_id
        )

        res.execute(sql, value)

        con.commit()

        flash("Supplier updated successfully.", "success")

        return redirect(url_for("supplier.supplier"))

    res = con.cursor()

    sql = """
    SELECT *
    FROM supplier
    WHERE supplier_id = ?
    """

    res.execute(sql, (supplier_id,))

    result = fetch_one_dict(res)

    return render_template(
        "update_supplier.html",
        data=result
    )


# ==========================================
# Delete Supplier
# ==========================================
@supplier_bp.route('/delete_supplier/<int:supplier_id>', methods=['GET', 'POST'])
def delete_supplier(supplier_id):

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    res = con.cursor()

    if request.method == 'POST':

        sql = """
        DELETE FROM supplier
        WHERE supplier_id = ?
        """

        res.execute(sql, (supplier_id,))

        con.commit()

        flash("Supplier deleted successfully.", "success")

        return redirect(url_for("supplier.supplier"))

    sql = """
    SELECT *
    FROM supplier
    WHERE supplier_id = ?
    """

    res.execute(sql, (supplier_id,))

    result = fetch_one_dict(res)

    return render_template(
        "delete_supplier.html",
        data=result
    )