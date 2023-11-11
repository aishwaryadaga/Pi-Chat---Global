from flask import Flask, render_template, request, jsonify, flash
from chat import *
from customchat import *
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError 
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import os
from flask import session
from dash_apps import *
from interview import *
from langflow_import import get_flow_response

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/files'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# CREATING USERS
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    

# FORMS
class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
           raise ValidationError(
               'That username already exists. Please choose a different one'
           ) 


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

    def authenticate(self):
        user = User.query.filter_by(username=self.username.data).first()
        if user and bcrypt.check_password_hash(user.password, self.password.data):
            return True
        return False

# FOR CUSTOM CHATBOT
class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

# FOR INTERVIEW ASSISTANT
class InterviewPrepForm(FlaskForm):
    choices = SelectField('Select your choice', choices=[('Data Science'), 
                                                         ('Machine Learning'), 
                                                         ('Deep Learning'), 
                                                         ('Artificial Intelligence')], 
                                                validators=[InputRequired()])


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'csv'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# DASH APPS
app1 = create_dash_app1(app)
app2 = create_dash_app2(app)
app3 = create_dash_app3(app)
# app4 = create_dash_app4(app)
# app5 = create_dash_app5(app)

# APP CONFIGURATION

# HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')

# LOGIN PAGE 
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.authenticate():
            user = User.query.filter_by(username=form.username.data).first()
            login_user(user)
            return redirect(url_for('main_page'))
        else:
            flash('Invalid login or password', 'errors')
    return render_template('login.html', form = form)

# ALL APPS DISPLAY
@app.route('/main', methods=['GET', 'POST'])
@login_required
def main_page():
    return render_template('main.html')


# LOGOUT
@app.route('/logout',methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# REGISTRATION PAGE
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form = form)

# GENERAL CHATBOT USING OPENAI (GPT-3.5-TURBO)
@app.route('/chatbot', methods=['GET', 'POST'])
@login_required
def chatbot():
    return render_template('chatbot.html')

# PREDICT ROUTE TO GET AI RESPONSE
@app.post("/predict")
@login_required
def predict():
    text = request.get_json().get("message")
    response = get_response(text)
    # create dict and then jsonify the response
    message = {"answer": response}
    return jsonify(message)

# CUSTOM CHATBOT
@app.route('/custom', methods=['GET', 'POST'])
@login_required
def custom():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        if allowed_file(file.filename):
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
            load_docs(file.filename)
            session['uploaded_filename'] = file.filename
            return render_template('customchat.html', form=form)
    return render_template('customchatupload.html', form=form)

# PREDICT ROUTE TO GET AI RESPONSE
@app.post("/custom_predict")
@login_required
def custom_predict():
    text = request.get_json().get("message")
    filename = session.get('uploaded_filename')
    response = get_custom_response(text, filename)
    message = {"answer": response}
    return jsonify(message)

# INTERVIEW ASSISTANT
@app.route("/interview", methods=['GET', 'POST'])
@login_required
def interview():
    form = InterviewPrepForm()
    if form.validate_on_submit():
        selected_choice = form.choices.data
        if selected_choice:
            create_prompt(data=selected_choice)
            return render_template('interview_ques.html', form=form)
        else:
            return render_template('interview.html', form=form)
    return render_template('interview.html', form=form)

# PREDICT ROUTE TO GET AI RESPONSE
@app.post("/interview_questions")
@login_required
def interview_questions():
    text = request.get_json().get("message")
    response = get_interview_question(text)
    message = {"answer": response}
    return jsonify(message)

# LANGFLOW CHATBOT
@app.route('/lf_chatbot', methods=['GET', 'POST'])
@login_required
def lf_chatbot():
    return render_template('lf_chatbot.html')

# PREDICT ROUTE TO GET AI RESPONSE
@app.post("/lf_predict")
@login_required
def lf_predict():
    text = request.get_json().get("message")
    response = get_flow_response(text)
    message = {"answer": response}
    return jsonify(message)

# DEMO VIDEO
@app.route('/demo', methods=['GET', 'POST'])
@login_required
def demo():
    return render_template('demo.html')

# RUN THE APP
if __name__ == "__main__":
    app.run(debug=True, port=5802)
    

# c:\Users\piuserintern\Desktop\Pi Chat - Global