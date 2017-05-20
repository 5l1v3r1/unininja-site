from flask import *
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_login import *
import datetime

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.session_protection = "strong"


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


class TimeForm(FlaskForm):
    working_time = HiddenField('Seconds', validators=[DataRequired()])
    submit = SubmitField('Submit')


class TasksForm(FlaskForm):
    """
    4 types:
    - Exam
        - User
        - Name
        - Subject
        - DateTime
        - Grade Percentage
        - Study time required
    - Assignment
        - User
        - Name
        - Subject
        - DateTime due
        - Complete before time
        - Grade Percentage
        - Time required
    - Lecture content
        - User
        - Name
        - Subject
        - DateTime Startweek
        - DateTime Stopweek
        - Grade Percentage
        - Time required
    - Task
        - User
        - Name
        - Details
        - Time required
    """

    name = StringField('Name', validators=[DataRequired()])
    length = StringField('Length', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class User(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(50), unique=True, index=True)
    password = db.Column('password', db.String(10))
    email = db.Column('email', db.String(50), unique=True, index=True)
    registered_on = db.Column('registered_on', db.DateTime)

    def __init__(self, username, password, email):
        self.name = username
        self.password = password
        self.email = email
        self.registered_on = datetime.datetime.utcnow()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % self.name


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    time = db.Column(db.Integer)

    def __repr__(self):
        return '<Task %r - %r>' % (self.id, self.name)


@app.route('/')
def index():
    return render_template('index.html', pagename='hi')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html', form=form)


@app.route('/work', methods=['GET', 'POST'])
def work():
    if session.get('time'):  # form submitted previously
        task, time_available = calculate_work()
        return render_template('work.html', task=task, time=time_available)

    form = TimeForm()
    if form.validate_on_submit():  # No form submitted
        session['time'] = form.working_time.data
        return redirect(url_for('work'))

    return render_template('input.html', form=form, action='work')


@app.route('/tasks', methods=['GET', 'POST'])
def input_tasks():
    tasks = Task.query.all()
    form = TasksForm()
    if form.validate_on_submit():
        task = Task(name=form.name.data, time=form.length.data)
        db.session.add(task)
        return redirect(url_for('input_tasks'))
    return render_template('tasks.html', form=form, tasks=tasks, action='tasks')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/material')
def material():
    tab = request.args.get('tab') or 'home'
    return render_template('material-base.html', tab=tab)


def calculate_work():
    return Task.query.first(), session.get('time')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
