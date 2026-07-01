from flask import Blueprint,session,render_template,request,redirect,url_for
#connect with database
from database import con
from helpers import fetch_all_dict, fetch_one_dict

auth_bp = Blueprint('auth',__name__)

@auth_bp.route('/register', methods=['GET','POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return render_template(
                'register.html',
                error="Password and Confirm Password do not match.",
                username = username
                )
        
        #Username check
        res = con.cursor()
        sql = 'select * from users where username=?'
        value = (username,)
        res.execute(sql,value)
        user = fetch_one_dict(res)

        if user:

            return render_template(
                'register.html',
                error="Username already exists.",
                username=username
            )
        #insert data
        res=con.cursor()
        sql = "INSERT INTO users(username, password) VALUES(?, ?)"
        value =(username,password)
        res.execute(sql,value)
        con.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html')

#Login Routes
@auth_bp.route('/', methods=['GET','POST'])
@auth_bp.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        res=con.cursor()
        sql='select * from users where username=?'
        value=(username,)
        res.execute(sql,value)

        user = fetch_one_dict(res)

        if user is None:
            
            return render_template(
                'login.html',
                error="Invalid Password.",
                username = username
            )
        
        if user["password"] != password:

            return render_template(
                "login.html",
                error="Invalid Password.",
                username=username
            )
        session["user"] = user["username"]

        return redirect(url_for("dashboard.home"))

    return render_template("login.html")

