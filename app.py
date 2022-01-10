import os
from re import template
from flask import Flask,abort,url_for,render_template,request,redirect,g
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, form
from sqlalchemy import Column, Integer, String, Float, Text,DateTime, BLOB,desc,asc, Boolean
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user
from flask_admin.menu import MenuLink
from PIL import Image
from config import setup_app, config_data
from model import User, Posts, Message,BulletinSuggestion,BulletinConcerns
from view import UserModelView,PostsModelView,MessageModelView,MessageModelView2,SuggestionModelView,SuggestionModelView2,ConcernModelView,ConcernModelView2
import random
import datetime

app = setup_app()
app.config['UPLOAD_FOLDER'] = config_data["upload_folder"]
app.config['MAX_CONTENT_PATH'] = config_data["max_upload_size"]

db = SQLAlchemy(app)
login = LoginManager(app)
user_details = {}


admin = Admin(app, name=config_data["app_admin_name"], template_mode=config_data["app_admin_template_mode"])
admin.add_view(UserModelView(User, db.session))
admin.add_view(PostsModelView(Posts,db.session, name='Posts'))
admin.add_view(SuggestionModelView(BulletinSuggestion,db.session,name='New Suggestions'))
admin.add_view(ConcernModelView(BulletinConcerns,db.session,name='New Concerns'))
admin.add_view(MessageModelView(Message,db.session,name='New Messages'))
admin.add_view(SuggestionModelView2(BulletinSuggestion,db.session,name='Approved Suggestions',endpoint='asuggest'))
admin.add_view(ConcernModelView2(BulletinConcerns,db.session,name='Approved Concerns',endpoint='aconcern'))
admin.add_view(MessageModelView2(Message,db.session,name='Replied Messages',endpoint='record'))
admin.add_link(MenuLink(name='Logout', category='', url="/logout"))

@app.context_processor
def default_contents():
    app_name = "SSU Student Council Page"
    #welcome page
    welcome_title = "Sorsogon State University Suggestion and Concern Portal"
    welcome_content = "Welcome to Student Council Page, this website is accessible to Sorsogon State University Bulan Campus Students. You can now login by using your student identification number  (ID), if you do not have account you can contact the student council officer to register your account. Take note: in using the student identification number we remove the dash (-) in your ID number, example username: 000000 and password: 000000. Students of Sorsogon State University Bulan Campus can only accessed this website by their default acccount."
    #student home page
    home_title = 'Student Council Bulletin Board'
    home_subtitle = 'Read the Latest Update Posts and, Approval for Suggestion and Concern by the Student Council'
    return dict(app_name=app_name,
                welcome_title=welcome_title,welcome_content=welcome_content,
                home_title=home_title,home_subtitle=home_subtitle)


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

## create database
@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created!')

## deleting database data
@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')

@app.route('/')
def welcome():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/validatelogin',methods=["POST","GET"])
def validatelogin():
    try:
        if request.method == "POST":
            username=request.form["username"]
            password=request.form["password"]
            try:
                user = User.query.filter_by(studentid=int(username)).one()
            except:
                user = User.query.filter_by(email=username).one()
            if ((username == str(user.email) or username == str(user.studentid)) and (password == user.password)):
                login_user(user)
                user_details = {}
                user_details.update({'id':user.id})
                user_details.update({'firstname': user.firstname})
                user_details.update({'middlename': user.middlename})
                user_details.update({'lastname': user.lastname})
                user_details.update({'studentid': user.studentid})
                user_details.update({'email': user.email})
                user_details.update({'access': user.access})

                if user.access == 'student':
                    return redirect(url_for("home"))
                elif user.access == 'admin':
                    return redirect(url_for("admin.index"))
            else:
                return render_template("request_submitted.html",message='Wrong Username or Password!')
    except Exception as e:
        return render_template("request_submitted.html",message='Invalid Cridentials')

@app.route('/validatesignup',methods=["POST","GET"])
def validatesignup():
    if request.method == 'POST':
        firstname = request.form['fname']
        middlename = request.form['mname']
        lastname = request.form['lname']
        studentid = request.form['studentid']
        email = request.form['email']
        password = request.form['password']
        rpassword = request.form['rpassword']

        if User.query.filter_by(studentid=int(studentid)).count() > 0:
            return render_template("request_submitted.html", message=f"username:{studentid} already in use.")
        elif User.query.filter_by(email=email).count() > 0:
            return render_template("request_submitted.html", message=f"email:{email} already in use.")
        elif password != rpassword:
            return render_template("request_submitted.html", message=f"Password does not match")
        else:
            add_signup = User(
                firstname = firstname,
                middlename=middlename,
                lastname=lastname,
                studentid=studentid,
                email=email,
                password=password,
                access='student'
            )
            db.session.add(add_signup)
            db.session.commit()
            return render_template("request_submitted.html", message=f"Signed Up Successfully")

    return render_template("request_submitted.html", message=f"Something Went Wrong!")

@app.route('/sendmessage',methods=["POST","GET"])
def sendmessage():
    if request.method == 'POST':
        message = request.form['message']
        studentid = current_user.studentid
        add_message = Message(
            studentid = studentid,
            message = message,
            reply = '',
            date = datetime.datetime.now()
        )
        db.session.add(add_message)
        db.session.commit()
    return redirect("contact")

@app.route("/contact")
def contact():
    account_name = User.query.filter_by(studentid=current_user.studentid).one()
    messages_record = Message.query.filter_by(studentid=current_user.studentid).all()
    return render_template("contact.html",messages_record=messages_record,account_name=account_name)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('welcome'))

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/home')
def home():
    posts = Posts.query.order_by(desc(Posts.date))
    posts_list = []
    i = 0
    for post in posts:
        if i >= 2:
            break
        else:
            posts_list.append(post)
        i += 1
    return render_template("studenthome.html",posts=posts_list,is_show_all=False)

@app.route('/showall')
def showall():
    posts = Posts.query.order_by(desc(Posts.date))
    return render_template("studenthome.html",posts=posts,is_show_all=True)

@app.route('/posts/<string:slug>')
def posts(slug):
    post = Posts.query.filter_by(slug=slug).one()
    return render_template("posts.html",post=post)

@app.route('/bulletin')
def bulletin():
    return render_template("bulletin.html")

@app.route('/bulletin_suggestions')
def bulletin_suggestions():
    return render_template("bulletin_suggestions.html")

@app.route('/sendsuggestions',methods=["POST","GET"])
def sendsuggestions():
    if request.method == 'POST':
        message = request.form['message']
        fullname = f'{current_user.firstname} {current_user.lastname}'
        add_message = BulletinSuggestion(
            requestee = fullname,
            message = message,
            date = datetime.datetime.now()
        )
        db.session.add(add_message)
        db.session.commit()
    return render_template("suggestion_submitted.html",message='Suggestion Sent Successfully!')


@app.route('/bulletin_concerns')
def bulletin_concerns():
    return render_template("bulletin_concerns.html")

@app.route('/sendconcerns',methods=["POST","GET"])
def sendconcerns():
    if request.method == 'POST':
        image = request.form['image']
        message = request.form['message']
        fullname = f'{current_user.firstname} {current_user.lastname}'
        add_message = BulletinConcerns(
            requestee = fullname,
            message = message,
            image = image,
            date = datetime.datetime.now()
        )
        db.session.add(add_message)
        db.session.commit()
    return render_template("suggestion_submitted.html",message='Concern Sent Successfully!')




if __name__ == "__main__":
    app.run(debug=True)