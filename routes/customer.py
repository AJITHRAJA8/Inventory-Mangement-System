from flask import Blueprint, render_template, request, redirect, url_for, session,flash
from database import con
from helpers import fetch_all_dict,fetch_one_dict
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

        ORDER BY customer_id 

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

        ORDER BY customer_id 

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

# ==========================================
# Add Customer
# ==========================================

@customer_bp.route('/add_customer', methods=['GET', 'POST'])
def add_customer():

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':

        customer_name = request.form['customer_name']

        phone = request.form['phone']

        email = request.form['email']

        address = request.form['address']

        # Check Duplicate Customer

        res = con.cursor()

        sql = """
        SELECT *

        FROM customer

        WHERE phone = ?
        """

        res.execute(sql, (phone,))

        customer = fetch_one_dict(res)

        if customer:

            return render_template(

                'add_customer.html',

                error='Phone number already exists.',

                data={

                    'customer_name': customer_name,

                    'phone': phone,

                    'email': email,

                    'address': address

                }

            )

        # Insert Customer

        sql = """
        INSERT INTO customer
        (
            customer_name,
            phone,
            email,
            address
        )

        VALUES
        (
            ?, ?, ?, ?
        )
        """

        value = (

            customer_name,

            phone,

            email,

            address

        )

        res.execute(sql, value)

        con.commit()

        flash(

            "Customer added successfully.",

            "success"

        )

        return redirect(

            url_for('customer.customer')

        )

    return render_template(

        'add_customer.html'

    )

# ==========================================
# Update Customer
# ==========================================

@customer_bp.route('/update_customer/<int:customer_id>', methods=['GET', 'POST'])
def update_customer(customer_id):

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':

        customer_name = request.form['customer_name']

        phone = request.form['phone']

        email = request.form['email']

        address = request.form['address']

        # Check Duplicate Phone

        res = con.cursor()

        sql = """
        SELECT *

        FROM customer

        WHERE phone = ?

        AND customer_id != ?
        """

        res.execute(sql, (phone, customer_id))

        customer = fetch_one_dict(res)

        if customer:

            return render_template(

                'update_customer.html',

                error='Phone number already exists.',

                data={

                    'customer_id': customer_id,

                    'customer_name': customer_name,

                    'phone': phone,

                    'email': email,

                    'address': address

                }

            )

        # Update Customer

        sql = """
        UPDATE customer

        SET

        customer_name=?,

        phone=?,

        email=?,

        address=?

        WHERE customer_id=?
        """

        value = (

            customer_name,

            phone,

            email,

            address,

            customer_id

        )

        res.execute(sql, value)

        con.commit()

        flash(

            "Customer updated successfully.",

            "success"

        )

        return redirect(

            url_for('customer.customer')

        )

    # Display Existing Customer

    res = con.cursor()

    sql = """
    SELECT *

    FROM customer

    WHERE customer_id=?
    """

    res.execute(sql, (customer_id,))

    customer = fetch_one_dict(res)

    return render_template(

        'update_customer.html',

        data=customer

    )

# ==========================================
# Delete Customer
# ==========================================

@customer_bp.route('/delete_customer/<int:customer_id>', methods=['GET', 'POST'])
def delete_customer(customer_id):

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    res = con.cursor()

    # -----------------------------
    # Check Foreign Key
    # -----------------------------

    sql = """
    SELECT *

    FROM stock_out

    WHERE customer_id = ?
    """

    res.execute(sql, (customer_id,))

    stock = fetch_one_dict(res)

    if stock:

        res = con.cursor()

        sql = """
        SELECT *

        FROM customer

        WHERE customer_id = ?
        """

        res.execute(sql, (customer_id,))

        customer = fetch_one_dict(res)

        return render_template(

            "delete_customer.html",

            data=customer,

            error="Cannot delete this customer because stock out records exist."

        )

    # -----------------------------
    # Delete Customer
    # -----------------------------

    if request.method == "POST":

        sql = """
        DELETE FROM customer

        WHERE customer_id = ?
        """

        res.execute(sql, (customer_id,))

        con.commit()

        flash(

            "Customer deleted successfully.",

            "success"

        )

        return redirect(

            url_for("customer.customer")

        )

    # -----------------------------
    # Display Customer
    # -----------------------------

    sql = """
    SELECT *

    FROM customer

    WHERE customer_id = ?
    """

    res.execute(sql, (customer_id,))

    customer = fetch_one_dict(res)

    return render_template(

        "delete_customer.html",

        data=customer

    )

