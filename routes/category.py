from flask import Blueprint, render_template, session, redirect, url_for, request,flash
from database import con
from helpers import fetch_all_dict, fetch_one_dict
import math

# Blueprint
category_bp = Blueprint('category', __name__)


# Category List + Search + Pagination
@category_bp.route('/category')
def category():

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    # Search
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

        # Total Search Records
        sql = "EXEC usp_Category_SearchCount ?"

        value = (search ,)

        res.execute(sql, value)

        total = fetch_one_dict(res)["total"]

        total_pages = math.ceil(total / per_page)

        # Search + Pagination
        sql = 'EXEC sp_SearchCategory ?, ?, ?'

        value = (
            search,
            offset,
            per_page
        )

        res.execute(sql, value)

    else:

        # Total Records
        sql = "EXEC usp_Category_Count"

        res.execute(sql)

        total = fetch_one_dict(res)["total"]

        total_pages = math.ceil(total / per_page)

        # Stored Procedure
        sql = "EXEC sp_GetCategories ?, ?"

        value = (
            offset,
            per_page
        )

        res.execute(sql, value)

    result = fetch_all_dict(res)

    return render_template(
        "category.html",
        datas=result,
        current_page=page,
        total_pages=total_pages,
        search=search
    )


# Add Category
@category_bp.route('/add_category', methods=['GET', 'POST'])
def add_category():

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':

        category_name = request.form['category_name']
        description = request.form['description']

        # Check Duplicate Category
        res = con.cursor()
        sql = 'EXEC usp_Category_GetByName ?'
        value = (category_name,)
        res.execute(sql, value)
        category = fetch_one_dict(res)

        if category:
            return render_template(
                'add_category.html',
                error='Category already exists.',
                category_name=category_name,
                description=description
            )

        res = con.cursor()

        sql = "EXEC usp_Category_Insert ?, ?"

        value = (
            category_name,
            description
        )

        res.execute(sql, value)

        con.commit()

        return redirect(url_for('category.category'))
    flash("Category added successfully.", "success")

    return render_template('add_category.html')


# Update Category
@category_bp.route('/update_category/<int:category_id>', methods=['GET', 'POST'])
def update_category(category_id):

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    res = con.cursor()

    if request.method == 'POST':

        category_name = request.form['category_name']
        description = request.form['description']

        # Check Duplicate Category

        sql = "EXEC usp_Category_GetByNameExcludingId ?, ?"

        value = (
            category_name,
            category_id
        )

        res.execute(sql, value)

        category = fetch_one_dict(res)

        if category:

            return render_template(
                'update_category.html',
                error='Category already exists.',
                data={
                    "category_id": category_id,
                    "category_name": category_name,
                    "description": description
                }
            )

        # Update Category
        sql = "EXEC usp_Category_Update ?, ?, ?"

        value = (
            category_name,
            description,
            category_id
        )

        res.execute(sql, value)

        con.commit()
        flash("Supplier updated successfully.", "success")

        return redirect(url_for('category.category'))

    # Display Current Category


    sql = "EXEC usp_Category_GetById ?"

    res.execute(sql, (category_id,))

    result = fetch_one_dict(res)

    return render_template(
        'update_category.html',
        data=result
    )

# Delete Category
@category_bp.route('/delete_category/<int:category_id>', methods=['GET', 'POST'])
def delete_category(category_id):

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    res = con.cursor()

    if request.method == 'POST':

        sql = "EXEC usp_Category_Delete ?"

        res.execute(sql, (category_id,))

        con.commit()

        return redirect(url_for('category.category'))

    sql = "EXEC usp_Category_GetById ?"

    res.execute(sql, (category_id,))

    result = fetch_one_dict(res)

    con.commit()

    flash("Category deleted successfully.", "success")

    return render_template(
        'delete_category.html',
        data=result
    )