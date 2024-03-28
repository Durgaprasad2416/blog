from flask import Flask,render_template,request,redirect,url_for,session
import mysql.connector
mydb=mysql.connector.connect(host="localhost",user="root",password="prasad",database="flaskblog")
with mysql.connector.connect(host="localhost",user="root",password="prasad",database="flaskblog"):
    cursor=mydb.cursor(buffered="True")
    cursor.execute("create table if not exists register(username varchar(50) primary key,Mobile varchar(20) unique,email varchar(50) unique,address varchar(50),password varchar(20))")

app=Flask(__name__)
app.secret_key="my secretkey is too secret"
@app.route("/")
def home():
    return render_template('homepage.html')
@app.route("/reg",methods=['GET','POST'])
def register():
    if request.method=="POST":
        Username=request.form['Username']
        Mobile=request.form['Mobile']
        Address=request.form['Address']
        Email=request.form['Email']
        Password=request.form['Password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('insert into register values(%s,%s,%s,%s,%s)',[Username,Mobile,Email,Address,Password])
        mydb.commit()
        cursor.close()
        return redirect(url_for('login'))
    return render_template('register.html')
@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=="POST":
        Username=request.form['Username']
        Password=request.form['Password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from register where username=%s && password=%s',[Username,Password])
        data=cursor.fetchone()[0]
        print(data)
        cursor.close()
        if data==1:
            session['Username']=Username
            if not session.get(session['Username']):
                session[session['Username']]={}
            return redirect(url_for('home'))
        else:
            return "Invalid Username and Password"
    return render_template("login.html")
@app.route('/logout')
def logout():
    if session.get('Username'):
        session.pop('Username')
    return redirect(url_for('login'))
@app.route('/admin')
def admin():
    return render_template('admin.html')
app.run()
