from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['SECRET_KEY'] = 'gymsecretkey'

# DATABASE CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# EMAIL CONFIG
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'premraj.aspirant@gmail.com'
app.config['MAIL_PASSWORD'] = 'fwtq iuaw usvr glwd'

db = SQLAlchemy(app)
mail = Mail(app)

# DATABASE MODEL
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

# HOME PAGE
@app.route('/')
def index():
    return render_template('index.html')

# LOGIN PAGE
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email, password=password).first()

        if user:
            flash('Login Successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid Credentials', 'danger')

    return render_template('login.html')

# REGISTER PAGE
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']

        new_user = User(
            fullname=fullname,
            email=email,
            password=password
        )

        db.session.add(new_user)
        db.session.commit()

        # SEND EMAIL
        msg = Message(
            'Gym Membership Enquiry Successful',
            sender='premraj.aspirant@gmail.com',
            recipients=[email]
        )

        msg.body = f"""
Hello {fullname},

Your enquiry for gym membership has been received successfully.

We will contact you soon.

Thank You
Fitness Pro Gym
"""

        mail.send(msg)

        flash('Registration Successful! Confirmation Email Sent.', 'success')

        return redirect(url_for('login'))

    return render_template('register.html')

# ADD MEMBER PAGE
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        plan = request.form['plan']

        return render_template(
            'success.html',
            name=name,
            age=age,
            plan=plan
        )

    return render_template('add.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
