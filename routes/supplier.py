from flask import Blueprint, render_template, session, redirect, url_for,request,flash
from database import con
from helpers import fetch_all_dict, fetch_one_dict

supplier_bp = Blueprint("supplier", __name__)

#supplier route
@supplier_bp.route('/supplier',methods=['GET','POST'])
def supplier():

    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    res = con.cursor()
    sql = 'select * from supplier order by supplier_id '
    res.execute(sql)
    result = fetch_all_dict(res)
    return render_template('supplier.html',datas=result)

# Add Supplier
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

        res = con.cursor()

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

        return redirect(url_for('supplier.supplier'))
    flash('Supplier added successfully!', 'success')

    return render_template('add_supplier.html')

#update supplier route
@supplier_bp.route('/update_supplier/<int:supplier_id>',methods=['GET','POST'])
def update_supplier(supplier_id):

    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':

        supplier_name = request.form['supplier_name']
        company_name = request.form['company_name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']

        #Check Duplicate Supplier
        sql = 'select * from supplier where supplier_name = ? and supplier_id != ?'
        res = con.cursor()
        value = (supplier_name,supplier_id)
        res.execute(sql,value)
        supplier = fetch_one_dict(res)

        if supplier:
            return render_template('update_supplier.html',
                                   error='Supplier already exists',
                                   data={
                                       'supplier_id': supplier_id,
                                        'supplier_name': supplier_name,
                                        'company_name': company_name,
                                        'phone': phone,
                                        'email': email,
                                        'address': address
                                   })
        # Update Supplier
        res = con.cursor()

        sql = 'update supplier set supplier_name = ?, company_name = ?, phone = ?, email = ?, address = ? where supplier_id = ?'
        value = (supplier_name, company_name, phone, email, address, supplier_id)
        res.execute(sql,value)
        con.commit()
        flash("Category updated successfully.", "success") 
        return redirect(url_for('supplier.supplier'))
    # Display Supplier
    res = con.cursor()
    sql = 'select * from supplier where supplier_id = ?'
    res.execute(sql,(supplier_id,))
    result = fetch_one_dict(res)
    return render_template('update_supplier.html',data=result)


#Delete Supplier
@supplier_bp.route('/delete_supplier/<int:supplier_id>',methods=['GET','POST'])
def delete_supplier(supplier_id):

    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    res = con.cursor()

    if request.method == 'POST':

        sql = 'delete from supplier where supplier_id = ?'

        res.execute(sql,(supplier_id,))

        con.commit()

        return redirect(url_for('supplier.supplier'))
    
    sql = 'select * from supplier where supplier_id = ?'

    res.execute(sql,(supplier_id,))

    result = fetch_one_dict(res)

    flash("Supplier deleted successfully.", "success")

    return render_template('delete_supplier.html',data=result)
