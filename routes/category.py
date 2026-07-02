from flask import Blueprint, render_template, session, redirect, url_for,request
from database import con
from helpers import fetch_all_dict,fetch_one_dict
from routes.auth import login

#Blueprint for category routes
category_bp = Blueprint('category',__name__)

#Route for category page
@category_bp.route('/category',methods=['GET','POST'])
def category():

    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    res=con.cursor()
    sql="SELECT * FROM category order by category_id"
    res.execute(sql)
    result=fetch_all_dict(res)
    return render_template('category.html',datas=result)

#Route for adding a new category
@category_bp.route('/add_category',methods=['GET','POST'])
def add_category():

    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':

        category_name = request.form['category_name']
        description = request.form['description']

        res = con.cursor()
        sql = 'insert into category(category_name,description) values(?,?)'
        values = (category_name, description)
        res.execute(sql, values)
        con.commit()
        return redirect(url_for('category.category'))
    return render_template('add_category.html')

#Route for editing a category
@category_bp.route('/update_category/<int:category_id>',methods=['GET','POST'])
def update_category(category_id):

    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        
        category_name = request.form['category_name']
        description = request.form['description']

        res = con.cursor()
        sql = 'update category set category_name=?, description=? where category_id=?'
        value = (category_name,description,category_id)
        res.execute(sql,value)
        con.commit()
        return redirect(url_for('category.category'))
    
    #display the current category data in the form
    res=con.cursor()
    sql='select * from category where category_id = ?'
    value=(category_id,)
    res.execute(sql,value)
    result=fetch_one_dict(res)
    return render_template('update_category.html',data=result)

#Route for deleting a category
@category_bp.route('/delete_category/<int:category_id>',methods=['GET','POST'])
def delete_category(category_id):

    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':

        res=con.cursor()
        sql = 'delete from category where category_id = ?'
        value = (category_id,)
        res.execute(sql,value)
        con.commit()
        return redirect(url_for('category.category'))
    
    #show the delete confirmation page
    res=con.cursor()
    sql = 'select * from category where category_id = ?'
    value =(category_id,)
    res.execute(sql,value)
    result = fetch_one_dict(res)
    return render_template('delete_category.html', data=result)

# Route for searching categories
@category_bp.route('/search_category', methods=['GET', 'POST'])
def search_category():

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    search = request.args.get('search')

    res = con.cursor()

    if search:

        sql = """
        SELECT *
        FROM category
        WHERE category_name LIKE ?
        ORDER BY category_id
        """

        value = ('%' + search + '%',)

        res.execute(sql, value)

    else:

        sql = """
        SELECT *
        FROM category
        ORDER BY category_id
        """

        res.execute(sql)

    result = fetch_all_dict(res)

    return render_template(
        'category.html',
        datas=result,
        search=search
    )