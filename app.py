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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new10.db'
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
from model import User, Firm, Role, feeds, questions, answers, Bonus, Mail, BonusFirm
from form import formRegisteration, loginForm, EditProfileForm, firmformRegisteration, firmloginForm, bonusForm, SearchForm, bonusFormf, SearchFormFirm

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
    #user_admin = User(username="bon.us.polito@gmail.com", usern="Bonus", name="Bonus", password=pass_c, isee=0,
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
        return redirect(url_for('login'))
    return render_template('register-db.html', regiterForm=regiterForm, name=name)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated == False:
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
    else:
        return redirect('dashboard')

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
        return render_template('profile.html', user_image=pic_profile, username=usern, user_isee=pic_isee,
                               user_job=pic_job, user_children=pic_children, isee=isee, age=age,
                               profession=profession, number_child=number_child)
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


@app.route('/account_details', methods=['GET', 'POST'])
@login_required
def account_details():
    if current_user.is_authenticated:
        user_details = current_user.user_variables()
        user = User.query.filter_by(id=current_user.id).first()
        if request.method == 'POST':
            updated_values_dict = request.form.to_dict()
            for k, v in updated_values_dict.items():
                if k == 'update_username':
                    user.username = v.rstrip()
                    session['email'] = user.username
                if k == 'update_usern':
                    user.usern = v.rstrip()
                    session['usern'] = user.usern
                if k == 'update_name':
                    user.name = v.rstrip()
                    session['name'] = user.name
                if k == 'update_isee':
                    user.isee = v.rstrip()
                    session['isee'] = user.isee
                if k == 'update_age':
                    user.age = v.rstrip()
                    session['age'] = user.age
                if k == 'update_profession':
                    user.profession = v.rstrip()
                    session['profession'] = user.profession
                if k == 'update_number_child':
                    user.number_child = v.rstrip()
                    session['number_child'] = user.number_child
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
    s = ''
    b1 = os.path.join(app.config['UPLOAD_FOLDER'], 'job.jpg')
    b2 = os.path.join(app.config['UPLOAD_FOLDER'], 'bonusvacanza.jpg')
    b3 = os.path.join(app.config['UPLOAD_FOLDER'], 'ecobonus110.jpg')
    b4 = os.path.join(app.config['UPLOAD_FOLDER'], 'BON-U$.png')
    b5 = os.path.join(app.config['UPLOAD_FOLDER'], 'BON-U$nosfondo.png')
    if current_user.is_authenticated:
        if session['user'] == True:
            s = session['email']
        else:
            s = session['emailf']

    return render_template('index.html', b1=b1, b2=b2, b3=b3, b4=b4, b5=b5, title=title, s=s)



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
    if current_user.is_authenticated == False:
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

    else:
        return redirect('dashboardfirm')

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
        return render_template('profilefirm.html', user_image=pic_profile, namef=namef, user_isee=pic_isee,
                               user_job=pic_job, user_children=pic_children, nemployees=nemployees, fatturato=fatturato,
                               sector=sector, piva=piva)
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
                    session['emailf'] = user.emailf
                if k == 'update_namef':
                    user.namef = v.rstrip()
                    session['namef'] = user.namef
                if k == 'update_nemployees':
                    user.nemployees = v.rstrip()
                    session['nemployees'] = user.nemployees
                if k == 'update_piva':
                    user.piva = v.rstrip()
                    session['piva'] = user.piva
                if k == 'update_sector':
                    user.sector = v.rstrip()
                    session['sector'] = user.sector
                if k == 'update_fatturato':
                    user.fatturato = v.rstrip()
                    session['fatturato'] = user.fatturato
            db.session.commit()
            return redirect(url_for('account_detailsf'))
    return render_template('account_detailsf.html', user_details=user_details)

@app.route('/404')
def notfound():
    pic = os.path.join(app.config['UPLOAD_FOLDER'], '404.png')

    return render_template('404.html', image=pic)

@app.route('/feedback')
def feedback():
    return render_template('feedback.html', values=feeds.query.all())

@app.route('/newFeedback', methods=["POST", "GET"])
@login_required
def newFeedback():
    if session['user'] == True:
        u = session['usern']
    else:
        u = session['namef']

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
        return render_template('newFeedback.html', u=u)

@app.route('/Newquestion' , methods=["POST", "GET"])
@login_required
def Newquestion():
    if session['user'] == True:
        u = session['usern']
    else:
        u = session['namef']

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
        return redirect('question')
    else:
        return render_template('question.html', u=u)

@app.route('/question' , methods=["POST", "GET"])
@login_required
def question():
    query = questions.query.all()
    return render_template('questions.html', values= query)

@app.route('/answer/<int:question_id>')
@login_required
def answer(question_id):
    if session['user'] == True:
        u = session['usern']
    else:
        u = session['namef']

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
    return render_template( 'answer.html', item=query, answers=queryAns, u=u)

@app.route('/NewAnswer' , methods=["POST", "GET"])
@login_required
def NewAnswer():
    if session['user'] == True:
        u = session['usern']
    else:
        u = session['namef']

    if request.method == "POST":
        idQ = request.form['idQ']
        userAnswer = request.form['userAnswer']
        if userAnswer == "" :
            flash("To submit correctly your answer add your username")
            return redirect('/answer/'+idQ, u=u)
        ans = request.form['answer']
        if ans == "" :
            flash("To submit correctly your answer add the answer")
            return redirect('/answer/'+idQ, u=u)


        a = answers(idQ, userAnswer, ans)
        db.session.add(a)
        db.session.commit()
        query = questions.query.filter_by(_id=request.form['idQ']).first()
        queryAns = answers.query.filter_by(idQ=request.form['idQ']).all()
        return render_template('/answer.html', item=query, answers=queryAns, u=u)
    else:
        return render_template('question.html', u=u)


@app.route('/addbonus', methods=['POST', 'GET'])
@login_required
def addbonus():
    if session['email'] == 'bon.us.polito@gmail.com':
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

    sbonus = model.Bonus.query.filter((model.Bonus.iseemin <= isee) & (model.Bonus.iseemax >= isee) &
                                      (model.Bonus.agemin <= age) & (model.Bonus.agemax >= age) &
                                      ((model.Bonus.professione == profession) | (model.Bonus.professione == 'qualsiasi') | (model.Bonus.professione == 'Qualsiasi')) &
                                      (model.Bonus.minfigli <= number_child) & (model.Bonus.maxfigli >= number_child))

    return render_template('bonusforyou.html', values=sbonus)


@app.route('/addbonusfirm', methods=['POST', 'GET'])
@login_required
def addbonusfirm():
    if session['email'] == 'bon.us.polito@gmail.com':
        name = None
        bonus_formf = bonusFormf()
        if bonus_formf.validate_on_submit():

            session['titolof'] = bonus_formf.titolof
            session['descrizionef'] = bonus_formf.descrizionef
            session['nemployeesmax'] = bonus_formf.nemployeesmax
            session['nemployeesmin'] = bonus_formf.nemployeesmin
            session['sector'] = bonus_formf.sector
            session['fatturatomax'] = bonus_formf.fatturatomax
            session['fatturatomin'] = bonus_formf.fatturatomin

            bonus = BonusFirm(titolof=bonus_formf.titolof.data, descrizionef=bonus_formf.descrizionef.data, nemployeesmax=bonus_formf.nemployeesmax.data,
                   nemployeesmin=bonus_formf.nemployeesmin.data, sector=bonus_formf.sector.data, fatturatomax=bonus_formf.fatturatomax.data, fatturatomin=bonus_formf.fatturatomin.data)
            db.session.add(bonus)
            db.session.commit()
            flash('successo')
            return redirect(url_for('confirm'))

        return render_template('addbonus-dbfirm.html', bonus_formf=bonus_formf, name_website='SQL Bonus to IS 2020 Platform', name=name)

    else:
        title = 'BON-U$'
        b1 = os.path.join(app.config['UPLOAD_FOLDER'], 'job.jpg')
        b2 = os.path.join(app.config['UPLOAD_FOLDER'], 'bonusvacanza.jpg')
        b3 = os.path.join(app.config['UPLOAD_FOLDER'], 'ecobonus110.jpg')
        b4 = os.path.join(app.config['UPLOAD_FOLDER'], 'BON-U$.png')
        b5 = os.path.join(app.config['UPLOAD_FOLDER'], 'BON-U$nosfondo.png')
        return render_template('index.html', b1 = b1, b2 = b2, b3 = b3, b4 = b4, b5 = b5, title = title)


@app.route('/bonuspagefirm', methods=['POST', 'GET'])
def searchfirm():
    form = SearchFormFirm()

    parola = form.searched.data

    if parola == None:
        sbonus = model.BonusFirm.query.filter(model.BonusFirm.descrizionef.like('%')).all()
    else:
        sbonus = model.BonusFirm.query.filter(model.BonusFirm.descrizionef.like('%'+parola+'%')).all()

    return render_template('searchfirm.html', form=form, sbonus=sbonus)


@app.route('/bonuspagefirm')
def bonuspagefirm():

    return render_template('bonuspagefirm.html', values=model.BonusFirm.query.all())


@app.route('/bonusforyoufirm')
@login_required
def bonusforyoufirm():
    nemployees = session['nemployees']
    sector = session['sector']
    fatturato = session['fatturato']
    user = session['user']

    sbonus = model.BonusFirm.query.filter((model.BonusFirm.nemployeesmin <= nemployees) & (model.BonusFirm.nemployeesmax >= nemployees) &
                                      (model.BonusFirm.fatturatomin <= fatturato) & (model.BonusFirm.fatturatomax >= fatturato) &
                                      ((model.BonusFirm.sector == sector) | (model.BonusFirm.sector == 'qualsiasi') | (model.BonusFirm.sector == 'Qualsiasi')))

    return render_template('bonusforyoufirm.html', values=sbonus)



@app.route('/contact', methods=['POST', 'GET'])
@login_required
def contact():
    image = os.path.join(app.config['UPLOAD_FOLDER'], 'BeFunky-design.png')
    if session['user'] == True:
        u = session['usern']
        m = session['email']
    else:
        u = session['namef']
        m = session['emailf']

    if request.method == "POST":
        username = request.form['username']
        if username == "" :
            flash("To submit correctly your question add your username")
            return redirect(request.url)

        ques = request.form['question']
        if ques == "" :
            flash("To submit correctly your questio add the question")
            return redirect(request.url)

        with app.app_context():

            msg = Message("Contact us",
                          sender="bon.us.polito@gmail.com",
                          recipients=["bon.us.polito.mail@gmail.com"])
            msg.body = "L'utente "+u+", con indirizzo mail "+m+" ha richiesto: "+ques
            mail.send(msg)


        return redirect('confirm')
    else:
        return render_template('contactus.html', u=u)


@app.route("/confirm")
def confirm():
    image = os.path.join(app.config['UPLOAD_FOLDER'], 'BeFunky-design1.jpg')
    return render_template('confirm.html', image=image)


@app.route("/confirm2")
def confirm2():
    image = os.path.join(app.config['UPLOAD_FOLDER'], '4.PNG')
    return render_template('confirm.html', image=image)


@app.route("/confirm3")
def confirm3():
    image = os.path.join(app.config['UPLOAD_FOLDER'], '3.jpg')
    return render_template('confirm.html', image=image)


@app.route("/newsletter", methods=['POST', 'GET'])
def newsletter():
    if request.method == "POST":
        mail = request.form['mail']
        if mail == "" :
            flash("Per iscriverti alla newsletter ti serve un indirizzo mail vaildo")
            return redirect(request.url)

        ma = Mail(mail=mail)
        db.session.add(ma)
        db.session.commit()

        return redirect("confirm2")

    return render_template("newsletter.html")


@app.route('/sendnews', methods=['POST', 'GET'])
@login_required
def sendnews():
    if session['email'] == 'bon.us.polito@gmail.com':

        if request.method == "POST":
            ques = request.form['ques']
            if ques == "":
                flash("To submit correctly your question add the question")
                return redirect(request.url)

            with app.app_context():

                all = model.Mail.query.all()
                s = '"'
                for item in all:
                    if s == '"':
                        s = '"' + item.__repr__()
                    else:
                        s = s + '", "' + item.__repr__()

                s = s+'"'
                print s

                #TODO risolvere le mail

                msg = Message("News Letter",
                              sender="bon.us.polito@gmail.com",
                              recipients=[s])  # tutte le mail
                msg.body = ques
                mail.send(msg)

            return redirect('confirm3')
        else:
            return render_template('sendnews.html')

    else:
        return render_template('404')



if __name__ == '__main__':
    app.run()
