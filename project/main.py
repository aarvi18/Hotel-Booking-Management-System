from flask import Flask, json,redirect,render_template,flash,request
from flask.globals import request, session
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

from flask_login import login_required,logout_user,login_user,login_manager,LoginManager,current_user
# import os
from flask_mail import Mail
import json


# mydatabase connection
local_server=True
app=Flask(__name__)
app.secret_key="aneesrehmankhan"

# with open('config.json','r') as c:
#   params=json.load(c)["params"]
# with open('../templates/config.json','r') as c:
#     params=json.load(c)["params"]



# app.config.update(
#     MAIL_SERVER='smtp.gmail.com',
#     MAIL_PORT=465,
#     MAIL_USE_SSL=True,
#     MAIL_USERNAME='eligiblerock@gmail.com',
#     MAIL_PASSWORD='Rahulsrock@123!'
# #     MAIL_USE_TLS = False
# #     MAIL_USE_SSL = True
# )
# mail = Mail(app)



# this is for getting the unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'

# app.config['SQLALCHEMY_DATABASE_URI']='mysql://username:password@localhost/databsename'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/hdms'
db=SQLAlchemy(app)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) or Hospitaluser.query.get(int(user_id))



class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))


class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    srfid=db.Column(db.String(20),unique=True)
    name=db.Column(db.String(20))
    email=db.Column(db.String(50))
    dob=db.Column(db.String(1000))
    password=db.Column(db.String(1000))
    cpassword=db.Column(db.String(1000))
    


class Hospitaluser(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    hcode=db.Column(db.String(20))
    email=db.Column(db.String(50))
    password=db.Column(db.String(1000))


class Hospitaldata(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    hcode=db.Column(db.String(20),unique=True)
    hname=db.Column(db.String(100))
    normalroom=db.Column(db.Integer)
    acroom=db.Column(db.Integer)
    nonacroom=db.Column(db.Integer)
    luxaryroom=db.Column(db.Integer)

class Trig(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    hcode=db.Column(db.String(20))
    normalroom=db.Column(db.Integer)
    acroom=db.Column(db.Integer)
    nonacroom=db.Column(db.Integer)
    luxaryroom=db.Column(db.Integer)
    querys=db.Column(db.String(50))
    date=db.Column(db.String(50))

class Bookingpatient(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    srfid=db.Column(db.String(20),unique=True)
    bedtype=db.Column(db.String(100))
    hcode=db.Column(db.String(20))
    spo2=db.Column(db.Integer)
    pname=db.Column(db.String(100))
    pphone=db.Column(db.String(100))
    paddress=db.Column(db.String(100))


@app.route("/")
def home():
   
    return render_template("index.html")

@app.route("/trigers")
def trigers():
    query=Trig.query.all() 
    return render_template("trigers.html",query=query)


@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=="POST":
        srfid=request.form.get('srf')
        name=request.form.get('name')
        email=request.form.get('email')
        dob=request.form.get('dob')
        password=request.form.get('password')
        cpassword=request.form.get('cpassword')
        # print(srfid,email,dob)
        encpassword=generate_password_hash(password)
        user=User.query.filter_by(srfid=srfid).first()
        emailUser=User.query.filter_by(email=email).first()
        if user or emailUser:
            flash("Email or srif is already taken","warning")
            return render_template("usersignup.html")
        new_user=db.engine.execute(f"INSERT INTO `user` (`srfid`,`name`,`email`,`dob`,`password`,`cpassword`) VALUES ('{srfid}','{name}','{email}','{dob}','{encpassword}','{cpassword}') ")
                
        flash("SignUp Success Please Login","success")
        return render_template("userlogin.html")

    return render_template("usersignup.html")


@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=="POST":
        # srfid=request.form.get('srf')
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","info")
            return render_template("index.html")
        else:
            flash("Invalid Credentials","danger")
            return render_template("userlogin.html")


    return render_template("userlogin.html")

@app.route('/hotellogin',methods=['POST','GET'])
def hotellogin():
    if request.method=="POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=Hospitaluser.query.filter_by(email=email).first()
        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","info")
            return render_template("index.html")
        else:
            flash("Invalid Credentials","danger")
            return render_template("hotellogin.html")


    return render_template("hotellogin.html")

@app.route('/admin',methods=['POST','GET'])
def admin():
 
    if request.method=="POST":
        username=request.form.get('username')
        password=request.form.get('password')
        if(username=='rahulsrock' and password=='rock123'):
            session['user']=username
            flash("login success","info")
            return render_template("addHosUser.html")
        else:
            flash("Invalid Credentials","danger")

    return render_template("admin.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('login'))



@app.route('/addHospitalUser',methods=['POST','GET'])
def hospitalUser():
   
    if('user' in session and session['user']=='rahulsrock'):
      
        if request.method=="POST":
            hcode=request.form.get('hcode')
            email=request.form.get('email')
            password=request.form.get('password')        
            encpassword=generate_password_hash(password)  
            # hcode=hcode.upper()      
            emailUser=Hospitaluser.query.filter_by(email=email).first()
            if  emailUser:
                flash("Email or srif is already taken","warning")
                return render_template("addHosUser.html")
            db.engine.execute(f"INSERT INTO `hospitaluser` (`hcode`,`email`,`password`) VALUES ('{hcode}','{email}','{encpassword}') ")

            # my mail starts from here if you not need to send mail comment the below line
           
            # mail.send_message('HOTEL MANAGEMENT CENTER',sender='eligiblerock@gmail.com',recipients=[email],body=f"Welcome thanks for choosing us\nYour Login Credentials Are:\n Email Address: {email}\nPassword: {password}\n\nHospital Code {hcode}\n\n Do not share your password\n\n\nThank You..." )

            flash("Data Sent and Inserted Successfully","warning")
            return render_template("addHosUser.html")

    else:
        flash("Login and try Again","warning")
        return render_template('/admin')
    


# testing wheather db is connected or not  
@app.route("/test")
def test():
    try:
        a=Test.query.all()
        print(a)
        return f'MY DATABASE IS CONNECTED'
    except Exception as e:
        print(e)
        return f'MY DATABASE IS NOT CONNECTED {e}'

@app.route("/logoutadmin")
def logoutadmin():
    session.pop('user')
    flash("You are logout admin", "primary")

    return redirect('/admin')


def updatess(code):
    postsdata=Hospitaldata.query.filter_by(hcode=code).first()
    return render_template("hospitaldata.html",postsdata=postsdata)

@app.route("/addhospitalinfo",methods=['POST','GET'])
def addhospitalinfo():
    email=current_user.email
    posts=Hospitaluser.query.filter_by(email=email).first()
    code=posts.hcode
    postsdata=Hospitaldata.query.filter_by(hcode=code).first()

    if request.method=="POST":
        hcode=request.form.get('hcode')
        hname=request.form.get('hname')
        normalroom=request.form.get('normalroom')
        acroom=request.form.get('acroom')
        nonacroom=request.form.get('nonacroom')
        luxaryroom=request.form.get('luxaryroom')
        # hcode=hcode.upper()
        huser=Hospitaluser.query.filter_by(hcode=hcode).first()
        hduser=Hospitaldata.query.filter_by(hcode=hcode).first()
        if hduser:
            flash("Data is already Present you can update it..","primary")
            return render_template("hospitaldata.html")
        if huser:            
            db.engine.execute(f"INSERT INTO `hospitaldata` (`hcode`,`hname`,`normalroom`,`acroom`,`nonacroom`,`luxaryroom`) VALUES ('{hcode}','{hname}','{normalroom}','{acroom}','{nonacroom}','{luxaryroom}')")
            flash("Data Is Added","primary")
            return redirect('/addhospitalinfo')
            

        else:
            flash("Hospital Code not Exist","warning")
            return redirect('/addhospitalinfo')




    return render_template("hospitaldata.html",postsdata=postsdata)

@app.route("/hedit/<string:id>",methods=['POST','GET'])
@login_required
def hedit(id):
    posts=Hospitaldata.query.filter_by(id=id).first()
  
    if request.method=="POST":
        hcode=request.form.get('hcode')
        hname=request.form.get('hname')
        normalroom=request.form.get('normalroom')
        acroom=request.form.get('acroom')
        nonacroom=request.form.get('nonacroom')
        luxaryroom=request.form.get('luxaryroom')
        hcode=hcode.upper()
        db.engine.execute(f"UPDATE `hospitaldata` SET `hcode` ='{hcode}',`hname`='{hname}',`normalroom`='{normalroom}',`acroom`='{acroom}',`nonacroom`='{nonacroom}',`luxaryroom`='{luxaryroom}' WHERE `hospitaldata`.`id`={id}")
        flash("Slot Updated","info")
        return redirect("/addhospitalinfo")

    posts=Hospitaldata.query.filter_by(id=id).first()
    return render_template("hedit.html",posts=posts)


@app.route("/hdelete/<string:id>",methods=['POST','GET'])
@login_required
def hdelete(id):
    db.engine.execute(f"DELETE FROM `hospitaldata` WHERE `hospitaldata`.`id`={id}")
    flash("Date Deleted","danger")
    return redirect("/addhospitalinfo")


@app.route("/pdetails",methods=['GET','POST'])
@login_required
def pdetails():
    code=current_user.hcode
    print(code)
    datas=db.engine.execute(f"SELECT `pname`,`bedtype`,`pphone`,`paddress` FROM `bookingpatient`,`hospitaldata` WHERE `bookingpatient`.`hcode`=`hospitaldata`.`hcode` and `hospitaldata`.`hcode`='{code}'")
    return render_template("detials.html",datas=datas)


@app.route("/slotbooking",methods=['POST','GET'])
@login_required
def slotbooking():
    query1=db.engine.execute(f"SELECT * FROM `hospitaldata` ")
    query=db.engine.execute(f"SELECT * FROM `hospitaldata` ")
    # query2=db.engine.execute(f"SELECT * FROM `hospitaldata` ")
    if request.method=="POST":
        
        srfid=request.form.get('srfid')
        bedtype=request.form.get('bedtype')
        hcode=request.form.get('hcode')
        spo2=request.form.get('spo2')
        pname=request.form.get('pname')
        pphone=request.form.get('pphone')
        paddress=request.form.get('paddress')  
        check2=Hospitaldata.query.filter_by(hcode=hcode).first()
        checkpatient=Bookingpatient.query.filter_by(srfid=srfid).first()
        if checkpatient:
            flash("already User is registered ","warning")
            return render_template("booking.html",query=query,query1=query1)
        
        if not check2:
            flash("Hospital Code not exist","warning")
            return render_template("booking.html",query=query,query1=query1)

        code=hcode
        dbb=db.engine.execute(f"SELECT * FROM `hospitaldata` WHERE `hospitaldata`.`hcode`='{code}' ")        
        bedtype=bedtype
        if bedtype=="normalroom":       
            for d in dbb:
                seat=d.normalroom
                print(seat)
                ar=Hospitaldata.query.filter_by(hcode=code).first()
                ar.normalroom=seat-1
                db.session.commit()
                
            
        elif bedtype=="acroom":      
            for d in dbb:
                seat=d.acroom
                print(seat)
                ar=Hospitaldata.query.filter_by(hcode=code).first()
                ar.acroom=seat-1
                db.session.commit()

        elif bedtype=="nonacroom":     
            for d in dbb:
                seat=d.nonacroom
                print(seat)
                ar=Hospitaldata.query.filter_by(hcode=code).first()
                ar.nonacroom=seat-1
                db.session.commit()

        elif bedtype=="luxaryrom": 
            for d in dbb:
                seat=d.luxaryrom
                ar=Hospitaldata.query.filter_by(hcode=code).first()
                ar.luxaryrom=seat-1
                db.session.commit()
        else:
            pass

        check=Hospitaldata.query.filter_by(hcode=hcode).first()
        if check!=None:
            if(seat>0 and check):
                res=Bookingpatient(srfid=srfid,bedtype=bedtype,hcode=hcode,spo2=spo2,pname=pname,pphone=pphone,paddress=paddress)
                db.session.add(res)
                db.session.commit()
                flash("Slot is Booked kindly Visit Hospital for Further Procedure","success")
                return render_template("booking.html",query=query,query1=query1)
            else:
                flash("Something Went Wrong","danger")
                return render_template("booking.html",query=query,query1=query1)
        else:
            flash("Give the proper hospital Code","info")
            return render_template("booking.html",query=query,query1=query1)
            
    
    return render_template("booking.html",query=query,query1=query1)
@app.route("/userdetails",methods=['POST','GET'])
@login_required    
def userdetails():
    po=current_user.srfid
    print(po)
    users=db.engine.execute(f"SELECT `bedtype`,`spo2`,`paddress`,`pphone` FROM `bookingpatient` WHERE `bookingpatient`.`srfid`='{po}'")
    return render_template("userdetails.html",users=users)
@app.route("/useredit",methods=['POST','GET'])
@login_required
def useredit():
    srfid=current_user.srfid
    posts=Bookingpatient.query.filter_by(srfid=srfid).first()
    if request.method=="POST":
        bedtype=request.form.get('bedtype')
        spo2=request.form.get('spo2')
        paddress=request.form.get('paddress')
        pphone=request.form.get('pphone')
        db.engine.execute(f"UPDATE `bookingpatient` SET `bedtype` ='{bedtype}',`spo2`='{spo2}',`paddress`='{paddress}',`pphone`='{pphone}' WHERE `bookingpatient`.`srfid`={srfid}")
        flash("Updated","info")
        return redirect("/userdetails")

    posts=Bookingpatient.query.filter_by(srfid=srfid).first()
    return render_template("hedit.html",posts=posts)
        




app.run(debug=True)
