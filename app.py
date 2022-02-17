from flask import Flask, render_template, redirect, url_for, session, flash, request
from flask_login import current_user, login_user, logout_user, login_required, login_manager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os, sqlite3
from flask_mail import Message,Mail
from flask_login import LoginManager
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)

#login = LoginManager(app)
#login.init_app(app)
#login.login_view = 'login'

app.config['SECRET_KEY'] = 'sssdhgclshfsh;shd;jshjhsjhjhsjldchljk'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new1.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# EMAIL config
app.config['MAIL_USERNAME']="" #os.environ['EMAIL_USERNAME']
app.config['MAIL_PASSWORD']=""
app.config['MAIL_TLS']=True
app.config['MAIL_SERVER']='smtp.mail.com'
app.config['MAIL_PORT']=587

app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <flasky@example.com>'

picFolder = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = picFolder



db = SQLAlchemy(app)
mail = Mail(app)
bcrypt = Bcrypt(app)
#db.create_all()
#os.chdir("try11\static")
#conn = sqlite3.connect("data.db")


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



from model import User, Firm, Role
from form import formRegisteration, loginForm, EditProfileForm, firmformRegisteration, firmloginForm

#EMAIL code
def send_mail(to,subject,template,**kwargs):
    msg=Message(subject,recipients=[to],sender=app.config['MAIL_USERNAME'])
    # msg.body= render_template(template + '.txt',**kwargs)
    msg.html= render_template(template + '.html',**kwargs)
    mail.send(msg)

@app.before_first_request
def setup_db():
    db.drop_all()
    db.create_all()
    role_admin = Role(role_name='Admin')
    role_user = Role(role_name='User')
    pass_c = bcrypt.generate_password_hash("Bon-U$2022")
    user_admin = User(username="andrea.calandra99@gmail.com", usern="Cally", name="Andrea", password=pass_c, isee=0,
                      age=0, profession="", number_child=0, role_name=role_admin)
    db.session.add_all([role_admin, role_user])
    db.session.add(user_admin)
    db.session.commit()
    #db.create_all()



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/signup', methods=['POST', 'GET'])
def regiterPagedb():
    name = None
    regiterForm = formRegisteration()
    if regiterForm.validate_on_submit():
        role_name = Role.query.filter_by(role_name="User").first()
        name = regiterForm.name.data
        usern = regiterForm.usern.data
        session['name'] = regiterForm.name.data
        session['email'] = regiterForm.email.data
        session['usern'] = regiterForm.usern.data
        session['isee'] = regiterForm.isee.data
        session['age'] = regiterForm.age.data
        session['profession'] = regiterForm.profession.data
        session['number_child'] = regiterForm.number_child.data
        password_2 = bcrypt.generate_password_hash(regiterForm.password.data).encode('utf-8')
        newuser = User(name=regiterForm.name.data, usern=regiterForm.usern.data, username=regiterForm.email.data,
                       password=password_2, isee=regiterForm.isee.data, age=regiterForm.age.data,
                       profession=regiterForm.profession.data, number_child=regiterForm.number_child.data, role_name=role_name)
        db.session.add(newuser)
        db.session.commit()
        #send_mail(regiterForm.email.data,"Welcome to BON-U$, registration successful ","mail",username=usern)

        # msg = Message("Hello",
        #               sender="bonus@gmail.com",
        #               recipients=["andrea.calandra99@gmail.com"])
        # msg.body = "hi"
        # msg.html = "<h1>test</h1>"

        # msg = Message('Hello', sender='bonus@gmail.com', recipients=['andrea.calandra99@gmail.com'])
        # msg.body = "Hello Flask message sent from Flask-Mail"
        # mail.send(msg)

        send_mail('andrea.calandra99@gmail.com', "New User!", "mail", username=usern)

        #mail.send(msg)

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
            session['isee'] = user_info.isee
            session['age'] = user_info.age
            session['profession'] = user_info.profession
            session['number_child'] = user_info.number_child
            login_user(user_info)
            return redirect('dashboard')

    return render_template('login.html', login_form=login_form)


@app.route('/dashboard')
@login_required
def dashboard():
    if session.get('email'):
        usern = session.get('usern')
        isee = session.get('isee')
        age = session.get('age')
        profession = session.get('profession')
        number_child = session.get('number_child')
        pic_profile = os.path.join(app.config['UPLOAD_FOLDER'], 'avatardefault.png')
        pic_isee = os.path.join(app.config['UPLOAD_FOLDER'], 'isee.jpg')
        pic_job = os.path.join(app.config['UPLOAD_FOLDER'], 'job.jpg')
        pic_children = os.path.join(app.config['UPLOAD_FOLDER'], 'children.jpg')
        return render_template('profile.html', user_image = pic_profile, username = usern, user_isee = pic_isee,
                               user_job = pic_job, user_children = pic_children, isee = isee, age = age,
                               profession = profession, number_child = number_child)
    else:
        return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('login'))  # =>redirect(index)


@app.route('/editProfile', methods=['GET', 'POST'])
@login_required
def editProfile():
    form = EditProfileForm(current_user.usern)
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.familyname = form.familyname.data
        current_user.usern = form.usern.data
        current_user.email = form.email.data
        current_user.password = form.password.data
        current_user.isee = form.isee.data
        current_user.age = form.age.data
        current_user.profession = form.profession.data
        current_user.number_child = form.number_child.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('editProfile'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.familyname.data = current_user.familyname
        form.usern.data = current_user.usern
        form.email.data = current_user.email
        form.password.data = current_user.password
        form.isee.data = current_user.isee
        form.age.data = current_user.age
        form.profession.data = current_user.profession
        form.number_child.data = current_user.number_child
    return render_template('editProfile.html', title='Edit Profile', form=form)


@app.route('/account_details', methods=['GET', 'POST'])
@login_required
def account_details():
    if current_user.is_authenticated:
        user_details = current_user.user_variables()
        user = User.query.filter_by(id=current_user.id).first()
        if request.method == 'POST':
            updated_values_dict = request.form.to_dict()
            for k, v in updated_values_dict.items():
                # TODO validation checks
                # TODO password change
                # The 'name' paramater in each form-control is jinja template of
                # update_{{user_details[key][0]}} hence the check for k == 'update_' etc.
                if k == 'update_username':
                    user.username = v.rstrip()
                if k == 'update_usern':
                    user.usern = v.rstrip()
                if k == 'update_name':
                    user.name = v.rstrip()
                if k == 'update_isee':
                    user.isee = v.rstrip()
                if k == 'update_age':
                    user.age = v.rstrip()
                if k == 'update_profession':
                    user.profession = v.rstrip()
                if k == 'update_number_child':
                    user.number_child = v.rstrip()
            db.session.commit()
            return redirect(url_for('account_details'))
    return render_template('account_details.html', user_details=user_details)


@app.route('/')
@app.route('/index')
def index():
    title = 'BON-U$'
    b1 = os.path.join(app.config['UPLOAD_FOLDER'], 'job.jpg')
    b2 = os.path.join(app.config['UPLOAD_FOLDER'], 'bonusvacanza.jpg')
    b3 = os.path.join(app.config['UPLOAD_FOLDER'], 'ecobonus110.jpg')
    b4 = os.path.join(app.config['UPLOAD_FOLDER'], 'BON-U$.png')
    b5 = os.path.join(app.config['UPLOAD_FOLDER'], 'BON-U$nosfondo.png')
    return render_template('index.html', b1 = b1, b2 = b2, b3 = b3, b4 = b4, b5 = b5, title = title)



# @app.route('/firmsignup', methods=['POST', 'GET'])
# def regiterPagedbFirm():
#     name = None
#     regiterForm = firmformRegisteration()
#     if regiterForm.validate_on_submit():
#         name = regiterForm.name.data
#         session['emailf'] = regiterForm.emailf.data
#         session['namef'] = regiterForm.namef.data
#         password_2 = bcrypt.generate_password_hash(regiterForm.passwordf.data).encode('utf-8')
#         session['nemployees'] = regiterForm.nemployees.data
#         session['piva'] = regiterForm.piva.data
#         session['sector'] = regiterForm.sector.data
#         session['fatturato'] = regiterForm.fatturato.data
#                         newfirm = Firm(emailf=regiterForm.emailf.data, namef=regiterForm.namef.data, nemployees=regiterForm.nemployees.data,
#                        password=password_2, piva=regiterForm.piva.data, sector=regiterForm.sector.data,
#                        fatturato=regiterForm.fatturato.data)
#         db.session.add(newfirm)
#         db.session.commit()
#         #send_mail(regiterForm.email.data,"Welcome to BON-U$, registration successful ","mail",username=usern)
#
#         msg = Message("Hello",
#                       sender="bonus@gmail.com",
#                       recipients=["andrea.calandra99@gmail.com"])
#         msg.body = "hi"
#         msg.html = "<h1>test</h1>"
#
#         #mail.send(msg)
#
#         flash('successo')
#         return redirect(url_for('firmlogin'))
#
#     return render_template('register-dbfirm.html', regiterForm=regiterForm, name_website='SQL Registration to IS 2020 Platform')
#
#
# @app.route('/firmlogin', methods=['POST', 'GET'])
# def login():
#     login_form = firmloginForm()
#     if login_form.validate_on_submit():
#         firm_info = Firm.query.filter_by(piva=login_form.piva.data).first()
#         if firm_info and bcrypt.check_password_hash(firm_info.passwordf, login_form.passwordf.data):
#             session['user_id'] = user_info.id
#             session['name'] = user_info.name
#             session['email'] = user_info.username
#             session['usern'] = user_info.usern
#             session['isee'] = user_info.isee
#             session['age'] = user_info.age
#             session['profession'] = user_info.profession
#             session['number_child'] = user_info.number_child
#
#             session['emailf'] = firm_info.emailf
#             session['namef'] = firm_info.namef
#             session['nemployees'] = firm_info.nemployees
#             session['piva'] = firm_info.piva
#             session['sector'] = firm_info.sector
#             session['fatturato'] = firm_info.fatturato
#
#             login_user(firm_info)
#             return redirect('dashboardfirm')
#
#     # return render_template('firmlogin.html', login_form=login_form)


if __name__ == '__main__':
    app.run()
