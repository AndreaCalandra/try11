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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new6.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# EMAIL config
# app.config['MAIL_USERNAME']="" #os.environ['EMAIL_USERNAME']
# app.config['MAIL_PASSWORD']=""
# app.config['MAIL_TLS']=True
# app.config['MAIL_SERVER']='smtp.mail.com'
# app.config['MAIL_PORT']=587
# app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
# app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <flasky@example.com>'
#MAX_CONTENT_PATH = '5120'
# app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
# app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
# app.config['MAIL_USERNAME'] = 'bon.us.polito@gmail.com'
# app.config['MAIL_PASSWORD'] = 'Bon-U$2022'
# app.config['MAIL_TLS']=True
# app.config['MAIL_SERVER']='smtp.mail.com'
# app.config['MAIL_PORT']=587

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_USERNAME'] = 'bon.us.polito@gmail.com'
app.config['MAIL_PASSWORD'] = 'Bon-U$2022'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_PORT'] = 587

mail = Mail(app)



picFolder = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = picFolder



db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
#db.create_all()
#os.chdir("try11\static")
#conn = sqlite3.connect("data.db")


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


import model
from model import User, Firm, Role, feeds, questions, answers, Bonus
from form import formRegisteration, loginForm, EditProfileForm, firmformRegisteration, firmloginForm, bonusForm, SearchForm

#EMAIL code
def send_mail(to,subject):
    msg=Message(subject,recipients=[to],sender='bon.us.polito@gmail.com')
    msg.body= 'Benvenuto'
    mail.send(msg)

@app.before_first_request
def setup_db():
    #db.drop_all()
    db.create_all()
    role_admin = Role(role_name='Admin')
    role_user = Role(role_name='User')
    pass_c = bcrypt.generate_password_hash("Bon-U$2022")
    #user_admin = User(username="andrea.calandra99@gmail.com", usern="Cally", name="Andrea", password=pass_c, isee=0,
    #                  age=0, profession="", number_child=0, role_name=role_admin)
    db.session.add_all([role_admin, role_user])
    #db.session.add(user_admin)
    #db.session.commit()
    #db.create_all()




@login_manager.user_loader
def load_user(user_id):
    if session['user']:
        return User.query.get(int(user_id))
    else:
        return Firm.query.get(int(user_id))



@app.route('/signup', methods=['POST', 'GET'])
def regiterPagedb():
    name = None
    regiterForm = formRegisteration()
    if regiterForm.validate_on_submit():
        role_name = Role.query.filter_by(role_name="User").first()
        session['name'] = regiterForm.name.data
        session['email'] = regiterForm.email.data
        session['usern'] = regiterForm.usern.data
        session['isee'] = regiterForm.isee.data
        session['age'] = regiterForm.age.data
        session['profession'] = regiterForm.profession.data
        session['number_child'] = regiterForm.number_child
        password_2 = bcrypt.generate_password_hash(regiterForm.password.data).encode('utf-8')
        newuser = User(name=regiterForm.name.data, usern=regiterForm.usern.data, username=regiterForm.email.data,
                       password=password_2, isee=regiterForm.isee.data, age=regiterForm.age.data,
                       profession=regiterForm.profession.data, number_child=regiterForm.number_child.data, role_name=role_name)
        db.session.add(newuser)
        db.session.commit()

        with app.app_context():
            msg = Message("Benvenuto",
                          sender="bon.us.polito@gmail.com",
                          recipients=[regiterForm.email.data])
            msg.html = render_template('mailReg.html')
            mail.send(msg)
        #send_mail(regiterForm.email.data,"Welcome to BON-U$")

        # msg = Message("Hello",
        #               sender="bonus@gmail.com",
        #               recipients=["andrea.calandra99@gmail.com"])
        # msg.body = "hi"
        # msg.html = "<h1>test</h1>"

        # msg = Message('Hello', sender='bonus@gmail.com', recipients=['andrea.calandra99@gmail.com'])
        # msg.body = "Hello Flask message sent from Flask-Mail"
        # mail.send(msg)

        #send_mail('andrea.calandra99@gmail.com', "New User!", "mail", username=regiterForm.email.data)

        #mail.send(msg)

        # msg = Message('CONTACT US',
        #               sender='jonpolito2018@gmail.com',
        #               recipients=['andrea.calandra99@gmail.com'])
        # msg.body = 'ciao'
        # mail.send(msg)

        return redirect(url_for('login'))

    return render_template('register-db.html', regiterForm=regiterForm, name=name)


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
            session['user'] = True

            login_user(user_info)
            return redirect('dashboard')

        else:
            flash("errore")
            return render_template('login.html', login_form=login_form)

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
    if session['user']:
        session.clear()
        logout_user()
        return redirect(url_for('login'))
    else:
        session.clear()
        logout_user()
        return redirect(url_for('firmlogin'))



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
                if k == 'update_password':
                    p = bcrypt.generate_password_hash(v.rstrip()).encode('utf-8')
                    user.password = p
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



@app.route('/firmsignup', methods=['POST', 'GET'])
def regiterPagedbFirm():
    name = None
    regiterFormFirm = firmformRegisteration()
    if regiterFormFirm.validate_on_submit():
        role_name = Role.query.filter_by(role_name="User").first()
        name = regiterFormFirm.namef.data
        session['emailf'] = regiterFormFirm.emailf.data
        session['namef'] = regiterFormFirm.namef.data
        password_2 = bcrypt.generate_password_hash(regiterFormFirm.passwordf.data).encode('utf-8')
        session['nemployees'] = regiterFormFirm.nemployees.data
        session['piva'] = regiterFormFirm.piva.data
        session['sector'] = regiterFormFirm.sector.data
        session['fatturato'] = regiterFormFirm.fatturato.data
        newfirm = Firm(emailf=regiterFormFirm.emailf.data, namef=regiterFormFirm.namef.data, nemployees=regiterFormFirm.nemployees.data,
                       passwordf=password_2, piva=regiterFormFirm.piva.data, sector=regiterFormFirm.sector.data,
                       fatturato=regiterFormFirm.fatturato.data, role_name=role_name)
        db.session.add(newfirm)
        db.session.commit()

        with app.app_context():
            msg = Message("Hello",
                          sender="bon.us.polito@gmail.com",
                          recipients=[regiterFormFirm.emailf.data])
            msg.html = render_template('mailReg.html')
            mail.send(msg)

        return redirect(url_for('firmlogin'))

    return render_template('register-dbfirm.html', regiterFormFirm=regiterFormFirm, name=name)


@app.route('/firmlogin', methods=['POST', 'GET'])
def firmlogin():
    login_form = firmloginForm()
    if login_form.validate_on_submit():
        firm_info = Firm.query.filter_by(piva=login_form.piva.data).first()
        if firm_info and bcrypt.check_password_hash(firm_info.passwordf, login_form.passwordf.data):
            session['emailf'] = firm_info.emailf
            session['namef'] = firm_info.namef
            session['nemployees'] = firm_info.nemployees
            session['piva'] = firm_info.piva
            session['sector'] = firm_info.sector
            session['fatturato'] = firm_info.fatturato
            session['user'] = False

            login_user(firm_info)
            return redirect('dashboardfirm')

    return render_template('firmlogin.html', login_form=login_form)


@app.route('/dashboardfirm')
@login_required
def dashboardfirm():
    if session.get('emailf'):
        namef = session.get('namef')
        nemployees = session.get('nemployees')
        fatturato = session.get('fatturato')
        sector = session.get('sector')
        piva = session.get('piva')
        pic_profile = os.path.join(app.config['UPLOAD_FOLDER'], 'avatardefault.png')
        pic_isee = os.path.join(app.config['UPLOAD_FOLDER'], 'isee.jpg')
        pic_job = os.path.join(app.config['UPLOAD_FOLDER'], 'job.jpg')
        pic_children = os.path.join(app.config['UPLOAD_FOLDER'], 'rev.jpg')
        return render_template('profilefirm.html', user_image = pic_profile, namef = namef, user_isee = pic_isee,
                               user_job = pic_job, user_children = pic_children, nemployees = nemployees, fatturato = fatturato,
                               sector = sector, piva = piva)
    else:
        return redirect(url_for('firmlogin'))


@app.route('/account_detailsf', methods=['GET', 'POST'])
@login_required
def account_detailsf():
    if current_user.is_authenticated:
        user_details = current_user.firm_variables()
        user = Firm.query.filter_by(id=current_user.id).first()
        if request.method == 'POST':
            updated_values_dict = request.form.to_dict()
            for k, v in updated_values_dict.items():
                # TODO validation checks
                # TODO password change
                # The 'name' paramater in each form-control is jinja template of
                # update_{{user_details[key][0]}} hence the check for k == 'update_' etc.
                if k == 'update_emailf':
                    user.emailf = v.rstrip()
                if k == 'update_namef':
                    user.namef = v.rstrip()
                if k == 'update_nemployees':
                    user.nemployees = v.rstrip()
                if k == 'update_piva':
                    user.piva = v.rstrip()
                if k == 'update_sector':
                    user.sector = v.rstrip()
                if k == 'update_fatturato':
                    user.fatturato = v.rstrip()
            db.session.commit()
            return redirect(url_for('account_detailsf'))
    return render_template('account_detailsf.html', user_details=user_details)

@app.route('/404')
def notfound():
    pic = os.path.join(app.config['UPLOAD_FOLDER'], '404.png')

    with app.app_context():

        msg = Message("Hello",
                      sender="bon.us.polito@gmail.com",
                      recipients=["andrea.calandra99@gmail.com",
                                  "sebastianodelnegro@gmail.com",
                                  "sordellosimone@gmail.com"])
        msg.html = render_template('mailReg.html')
        mail.send(msg)

    return render_template('404.html', image=pic)

@app.route('/feedback')
def feedback():
    return render_template('feedback.html', values=feeds.query.all())

@app.route('/newFeedback', methods=["POST", "GET"])
def newFeedback():
    if request.method == "POST":
        username = request.form['username']
        if username == "" :
            flash("To submit correctly your feedback add your username")
            return redirect(request.url)

        feedback = request.form['feedback']
        if feedback == "" :
            flash("To submit correctly your feedback add your feedback")
            return redirect(request.url)

        feed = feeds(username, feedback)
        db.session.add(feed)
        db.session.commit()
        return redirect('feedback')
    else:
        return render_template('newFeedback.html')

@app.route('/Newquestion' , methods=["POST", "GET"])
def Newquestion():
    if request.method == "POST":
        username = request.form['username']
        if username == "" :
            flash("To submit correctly your question add your username")
            return redirect(request.url)

        ques = request.form['question']
        if ques == "" :
            flash("To submit correctly your questio add the question")
            return redirect(request.url)

        q = questions(username, ques)
        db.session.add(q)
        db.session.commit()
        u = session['usern']
        return redirect('question', u=u)
    else:
        return render_template('question.html')

@app.route('/question' , methods=["POST", "GET"])
def question():
    query = questions.query.all()
    return render_template('questions.html', values= query)

@app.route('/answer/<int:question_id>')
def answer(question_id):
    if request.method == "POST":
        userAnswer = request.form['userAnswer']
        if userAnswer == "" :
            flash("To submit correctly your answer add your username")
            return redirect(request.url)
        ans = request.form['answer']
        if ans == "" :
            flash("To submit correctly your answer add the answer")
            return redirect(request.url)

        idQ = request.form['idQ']
        a = answers(idQ, userAnswer, ans)
        db.session.add(a)
        db.session.commit()
    query = questions.query.filter_by(_id=question_id).first()
    queryAns = answers.query.filter_by(idQ=question_id).all()
    return render_template( 'answer.html', item=query, answers=queryAns)

@app.route('/NewAnswer' , methods=["POST", "GET"])
def NewAnswer():
    if request.method == "POST":
        idQ = request.form['idQ']
        userAnswer = request.form['userAnswer']
        if userAnswer == "" :
            flash("To submit correctly your answer add your username")
            return redirect('/answer/'+idQ)
        ans = request.form['answer']
        if ans == "" :
            flash("To submit correctly your answer add the answer")
            return redirect('/answer/'+idQ)


        a = answers(idQ, userAnswer, ans)
        db.session.add(a)
        db.session.commit()
        query = questions.query.filter_by(_id=request.form['idQ']).first()
        queryAns = answers.query.filter_by(idQ=request.form['idQ']).all()
        return render_template('/answer.html', item=query, answers=queryAns)
    else:
        return render_template('question.html')


@app.route('/addbonus', methods=['POST', 'GET'])
@login_required
def addbonus():
    if session['email'] == 'andrea.calandra99@gmail.com':
        name = None
        bonus_form = bonusForm()
        if bonus_form.validate_on_submit():

            session['titolo'] = bonus_form.titolo
            session['descrizione'] = bonus_form.descrizione
            session['iseemin'] = bonus_form.iseemin
            session['iseemax'] = bonus_form.iseemax
            session['agemax'] = bonus_form.agemax
            session['agemin'] = bonus_form.agemin
            session['maxfigli'] = bonus_form.maxfigli
            session['minfigli'] = bonus_form.minfigli
            session['professione'] = bonus_form.professione
            bonus = Bonus(titolo=bonus_form.titolo.data, descrizione=bonus_form.descrizione.data, iseemin=bonus_form.iseemin.data,
                   iseemax=bonus_form.iseemax.data, agemax=bonus_form.agemax.data, agemin=bonus_form.agemin.data, maxfigli=bonus_form.maxfigli.data, minfigli=bonus_form.minfigli.data,professione=bonus_form.professione.data)
            db.session.add(bonus)
            db.session.commit()
            flash('successo')
            return redirect(url_for('dashboard'))

        return render_template('addbonus-db.html', bonus_form=bonus_form, name_website='SQL Bonus to IS 2020 Platform', name=name)

    else:
        title = 'BON-U$'
        b1 = os.path.join(app.config['UPLOAD_FOLDER'], 'job.jpg')
        b2 = os.path.join(app.config['UPLOAD_FOLDER'], 'bonusvacanza.jpg')
        b3 = os.path.join(app.config['UPLOAD_FOLDER'], 'ecobonus110.jpg')
        b4 = os.path.join(app.config['UPLOAD_FOLDER'], 'BON-U$.png')
        b5 = os.path.join(app.config['UPLOAD_FOLDER'], 'BON-U$nosfondo.png')
        return render_template('index.html', b1 = b1, b2 = b2, b3 = b3, b4 = b4, b5 = b5, title = title)

@app.route('/bonuspage', methods=['POST', 'GET'])
def search():
    form = SearchForm()

    parola = form.searched.data

    if parola == None:
        sbonus = model.Bonus.query.filter(model.Bonus.descrizione.like('%')).all()
    else:
        sbonus = model.Bonus.query.filter(model.Bonus.descrizione.like('%'+parola+'%')).all()

    return render_template('search.html', form=form, sbonus=sbonus)


@app.route('/bonuspage')
def bonuspage():

    return render_template('bonuspage.html', values=model.Bonus.query.all())


@app.route('/bonusforyou')
@login_required
def bonusforyou():
    name = session['name']
    email = session['email']
    username = session['usern']
    isee = session['isee']
    age = session['age']
    profession = session['profession']
    number_child = session['number_child']
    user = session['user']

    sbonus = model.Bonus.query.filter((isee >= model.Bonus.iseemin) & (isee <= model.Bonus.iseemax) &
                                      (age >= model.Bonus.agemin) & (age <= model.Bonus.agemax) &
                                      ((profession == model.Bonus.professione) | (profession == 'qualsiasi') | (profession == 'Qualsiasi')) &
                                      (number_child >= model.Bonus.minfigli) & (number_child <= model.Bonus.maxfigli))

    return render_template('bonusforyou.html', values=sbonus)

if __name__ == '__main__':
    app.run()
