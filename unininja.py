from flask import *
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_login import *
from requests_oauthlib import OAuth2Session
from requests import HTTPError
from config import Auth
import datetime

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.session_protection = "strong"


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


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    avatar = db.Column(db.String(200))
    active = db.Column(db.Boolean, default=False)
    tokens = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())


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


@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    google = get_google_auth()
    auth_url, state = google.authorization_url(
        Auth.AUTH_URI, access_type='offline')
    session['oauth_state'] = state
    return render_template('login.html', auth_url=auth_url)


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


@app.route('/gCallback')
def callback():
    # Redirect user to home page if already logged in.
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('index'))
    if 'error' in request.args:
        if request.args.get('error') == 'access_denied':
            return 'You denied access.'
        return 'Error encountered.'
    if 'code' not in request.args and 'state' not in request.args:
        return redirect(url_for('login'))
    else:
        # Execution reaches here when user has
        # successfully authenticated our app.
        google = get_google_auth(state=session.get('oauth_state'))
        try:
            token = google.fetch_token(
                Auth.TOKEN_URI,
                client_secret=Auth.CLIENT_SECRET,
                authorization_response=request.url)
        except HTTPError:
            return 'HTTPError occurred.'
        google = get_google_auth(token=token)
        resp = google.get(Auth.USER_INFO)
        if resp.status_code == 200:
            user_data = resp.json()
            email = user_data['email']
            user = User.query.filter_by(email=email).first()
            if user is None:
                user = User()
                user.email = email
            user.name = user_data['name']
            print(token)
            user.tokens = json.dumps(token)
            user.avatar = user_data['picture']
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('index'))
        return 'Could not fetch your information.'


def get_google_auth(state=None, token=None):
    if token:
        return OAuth2Session(Auth.CLIENT_ID, token=token)
    if state:
        return OAuth2Session(
            Auth.CLIENT_ID,
            state=state,
            redirect_uri=Auth.REDIRECT_URI)
    oauth = OAuth2Session(
        Auth.CLIENT_ID,
        redirect_uri=Auth.REDIRECT_URI,
        scope=Auth.SCOPE)
    return oauth


def calculate_work():
    return Task.query.first(), session.get('time')


if __name__ == '__main__':
    app.run(debug=True)
