from flask import Flask, session, render_template, request, redirect, url_for, g, flash
import os
from admin_table import admin_table
from app_table import app_table
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://lumlcggnjdaumc:f276602e62d3bea9ed337e0d364be3d052e5649d1efacf7b8cbdbcc468970929@ec2-54-221-201-212.compute-1.amazonaws.com:5432/d8p1th5vv9dmeu'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db=SQLAlchemy(app)

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'bcsf16a030@pucit.edu.pk',
    "MAIL_PASSWORD": '########'
}

app.config.update(mail_settings)
mail = Mail(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

admin_data = admin_table()
app_data=app_table()


class Scheduled(db.Model):
    __tablename__ = 'scheduled'
    app_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(200))
    email = db.Column(db.String(1000))
    time = db.Column(db.Time)
    date = db.Column(db.Date)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/admin')
def admin():
    if g.user:
        return render_template('admin.html')

    return redirect(url_for('login'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.pop('user', None)

        if request.form['password'] == admin_data.getPassword() and request.form['username'] == admin_data.getUser():
            session['user'] = request.form['username']
            return redirect(url_for('admin'))
        else:

            return redirect(url_for('status',status='Login',message='Username or Password is incorrect'))

    return render_template('login.html')


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route('/menu')
def menu():
    return render_template('admin.html')

@app.route('/status<status>/<message>')
def status(status,message):
    return render_template('status.html',status=status,message=message)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/appointment')
def appointment():
    return render_template('appointment.html')


@app.route('/signout')
def signout():
    session.pop('user', None)

    return redirect(url_for('index'))

@app.route('/editAccount',methods=['GET','POST'])
def editAccount():
    if g.user:
        if request.method=='POST':
            if request.form['password'] == admin_data.getPassword() and request.form['username'] == admin_data.getUser():
                return redirect(url_for('adminAccount'))
            else:
                 return redirect(url_for('status',status='Edit Account',message='Username or Password is incorrect'))

        return render_template('editAccount.html')
    else:
        return redirect(url_for('login'))


@app.route('/adminAccount')
def adminAccount():
   if g.user:
     return render_template('changeAccount.html')
   else:
       return redirect(url_for('login'))

@app.route('/changeAccount',methods=['POST'])
def changeAccount():
    if request.method=='POST':
        user=request.form['Nuser']
        n_password=request.form['Npassword']
        admin_data.setUser(user,n_password)
    return redirect(url_for('login'))


@app.route('/appointments')
def appointments():
    if g.user:
        appointments=app_data.getAll()
        return render_template('appointments.html',appointments=appointments)
    else:
        return redirect(url_for('login'))


@app.route('/appointments/submit',methods=['POST'])
def addAppointments():
    name=request.form["name"]

    phoneNo=request.form["phone"]

    gender=request.form["gender"]

    age=request.form["birthDate"]

    address=request.form["address"]

    email=request.form["email"]

    type = request.form["type"]


    app_data.addAppointment(name,phoneNo,gender,age,address,email,type)

    return redirect(url_for("appointment"))





@app.route('/scheduled')
def scheduled():
    if g.user:
        sched=Scheduled.query.all()
        return render_template('scheduled.html',sched=sched)
    else:
        return redirect(url_for('login'))


@app.route('/editPatients')
def editPatient():
    if g.user:
        return render_template('editPatients.html')
    else:
        return redirect(url_for('login'))


@app.route('/updateInfo<id>',methods=['POST','GET'])
def updateInfo(id):
    if g.user:
        return render_template('updateInfo.html')
    else:
        return redirect(url_for('login'))

@app.route('/appointments/scheduled/<id>',methods=['POST'])
def sendEmail(id):

    date=request.form['date']
    time=request.form['time']
    app=app_data.getSpecific(id)
    info = Scheduled(name=app[1], email=app[6], gender=app[3], age=app[4],time=time,date=date)
    db.session.add(info)
    db.session.commit()
<<<<<<< HEAD
=======
    app_data.deleteAppointment(id)
>>>>>>> b866ef1

    message="Hi,you have been scheduled for an appointment at "+time+" on "+date+". Thanks "
  #  msg = Message("Appointment Reserved at HealthPatron",
   #               sender="bcsf16a030@pucit.edu.pk",
    #                  recipients=[email])
   # msg.body = message
    #mail.send(msg)

    return redirect(url_for("admin"))



if __name__ == '__main__':
    manager.run()
