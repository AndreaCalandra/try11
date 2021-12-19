from flask import Flask, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os, sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sssdhgclshfsh;shd;jshjhsjhjhsjldchljk'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
#db.create_all()
#os.chdir("try11\static")
#conn = sqlite3.connect("data.db")

from model import User
from form import formRegisteration, loginForm

@app.before_first_request
def setup_db():
    #db.drop_all()
    #session.clear()
    db.create_all()


@app.route('/', methods=['POST', 'GET'])
def regiterPagedb():
    name = None
    regiterForm = formRegisteration()
    if regiterForm.validate_on_submit():
        name = regiterForm.name.data
        session['name'] = regiterForm.name.data
        session['email'] = regiterForm.email.data
        session['usern'] = regiterForm.usern.data
        password_2 = bcrypt.generate_password_hash(regiterForm.password.data).encode('utf-8')
        newuser = User(name=regiterForm.name.data, usern=regiterForm.usern.data, username=regiterForm.email.data, password=password_2)
        db.session.add(newuser)
        db.session.commit()
        flash('successo')
        return redirect(url_for('login'))
    return render_template('register-db.html', regiterForm=regiterForm, name_website='SQL Registration to IS 2020 Platform', name=name)


@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = loginForm()
    if login_form.validate_on_submit():
        user_info = User.query.filter_by(username=login_form.username.data).first()
        if user_info and bcrypt.check_password_hash(user_info.password, login_form.password.data):
            session['user_id'] = user_info.id
            session['name'] = user_info.name
            session['email'] = user_info.username
            session['usern'] = user_info.usern
            return redirect('dashboard')

    return render_template('login.html', login_form=login_form)


@app.route('/dashboard')
def dashboard():
    if session.get('email'):
        name = session.get('name')
        return render_template('dashboard.html', name=name)
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('posthtml_layout'))  # =>redirect(index)

if __name__ == '__main__':
    app.run()
