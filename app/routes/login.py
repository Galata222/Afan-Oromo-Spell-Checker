from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators

from flask_sqlalchemy import SQLAlchemy

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)



# db = SQLAlchemy(app)  # Create SQLAlchemy instance with the Flask app directly

login_routes = Blueprint('login_routes', __name__)

@login_routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    submit = SubmitField('Login')

@app.route('/')
def home():
    return "Welcome to the home page!"

if __name__ == '__main__':
    db.create_all()
    app.register_blueprint(login_routes)
    app.run(debug=True)
