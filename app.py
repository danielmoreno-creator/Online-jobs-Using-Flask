from flask import Flask, render_template, redirect, url_for, request, flash
from pymongo import MongoClient
from bson import ObjectId
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Set up the MongoDB connection
client = MongoClient("mongodb://localhost:27017")
db = client['job_board']

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Define the User class for authentication
class User(UserMixin):
    def __init__(self, user_id, username, email, password):
        self.id = user_id
        self.username = username
        self.email = email
        self.password = password

    def save(self):
        # Save the user to the database
        user_data = {
            "username": self.username,
            "email": self.email,
            "password": self.password
        }
        db.users.insert_one(user_data)

# Define a form for user registration
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

@login_manager.user_loader
def load_user(user_id):
    # Replace this with your user loading logic from MongoDB
    user_data = db.users.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return User(user_id, user_data['username'], user_data['email'], user_data['password'])
    return None

# Add the index route (Login Page)
@app.route('/', methods=['GET', 'POST'])
def login():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Add your login logic here
        user_data = db.users.find_one({"email": form.email.data})
        if user_data and bcrypt.check_password_hash(user_data['password'], form.password.data):
            user = User(user_data['_id'], user_data['username'], user_data['email'], user_data['password'])
            login_user(user)
            return redirect(url_for('index'))

        flash('Login failed. Please check your credentials.', 'danger')

    return render_template('login.html', form=form)

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Hash the user's password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # Create a new user
        new_user = User(None, form.username.data, form.email.data, hashed_password)

        # Save the user to the database
        new_user.save()

        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
