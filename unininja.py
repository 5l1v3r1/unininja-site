import os
import enum
from datetime import datetime
from urllib.parse import urlparse, urljoin

from flask import *
from flask_sqlalchemy import SQLAlchemy  # Prevents SQL injection by default
from flask_login import LoginManager, current_user, login_user, logout_user, UserMixin

from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField, PasswordField
from wtforms.validators import DataRequired

from passlib.hash import sha256_crypt
SALT = "4ec82967c2f3317b"

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)



@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


class TimeForm(FlaskForm):
    working_time = HiddenField('Seconds', validators=[DataRequired()])
    submit = SubmitField('Submit')


class SignupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(255), unique=True)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())

    tasks = db.relationship("Task", backref='users')


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(64))
    subject = db.Column(db.String(64))
    details = db.Column(db.UnicodeText())
    type = db.Column(db.Enum('exam', 'assignment', 'task', name='task_type'))
    due_time = db.Column(db.Integer)
    percent_complete = db.Column(db.Integer)
    percent_worth = db.Column(db.Integer)

    def __repr__(self):
        return '<Task %r - %r>' % (self.id, self.name)


def create_user(name, email, password):
    password = sha256_crypt.hash(password, salt=SALT)
    if not User.query.filter_by(email=email).first():
        user = User(name=name, email=email, password=password, active=True, confirmed_at=datetime.utcnow())
        db.session.add(user)
        db.session.commit()
        return True
    else:
        return False


def check_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user:
        if sha256_crypt.verify(password, user.password):
            return user
        else:
            return None
    else:
        return None


@app.before_request
def before_request():
    if request.url.startswith('http://') and not request.url.startswith("http://127.0.0."):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)


@app.route('/')
def index():
    if current_user.is_authenticated:
        tab = request.args.get('tab') or 'home'

        tasks = Task.query.filter_by(user_id=current_user.id).all()
        tasks = filter_tasks(tasks)
        tasks = calculate_work(tasks)

        return render_template('index.html', tab=tab, tasks=tasks)
    else:
        return render_template('unregistered.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        if create_user(form.name.data, form.email.data, form.password.data):
            return redirect(url_for('index'))
        else:
            flash("Could not create user")
            return render_template('signup.html', form=form)
    return render_template('signup.html', form=form)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@app.route('/login', methods=['GET', 'POST'])
def login():
    logout_user()
    form = LoginForm()
    if form.validate_on_submit():
        user = check_user(form.email.data, form.password.data)
        if user:
            login_user(user, remember=True)

            next_redir = request.args.get('next')
            if not is_safe_url(next_redir):
                return abort(400)

            return redirect(url_for('index'))
        else:
            session['user'] = None
            return render_template('login.html', form=form, error=True)
    return render_template('login.html', form=form, error=False)


def filter_tasks(raw_tasks):
    tasks = []
    for raw_task in raw_tasks:
        task = {'id': raw_task.id,
                'name': raw_task.name,
                'subject': raw_task.subject,
                'details': raw_task.details,
                'due_time': raw_task.due_time,
                'percent_complete': raw_task.percent_complete,
                'percent_worth': raw_task.percent_worth
                }
        tasks.append(task)
    return tasks


@app.route('/work', methods=['GET', 'POST'])
def work():
    time = request.args.get('time')
    if current_user.is_authenticated and time:
        tasks = Task.query.filter_by(user_id=current_user.id).all()
        tasks = filter_tasks(tasks)
        tasks = calculate_work(tasks)
        if len(tasks) < 1:
            return redirect('/?tab=assignments')
        return render_template('work.html', task=tasks[0], time=time)

    else:
        return redirect('/')


@app.route('/tasks')
def input_tasks():
    args = request.args
    type = args['type']

    tasks = Task.query.filter_by(user_id=current_user.id, type=type).all()
    tasks = filter_tasks(tasks)

    tasks = calculate_work(tasks)

    return jsonify({'status': 'success',
                    'tasks': tasks})


@app.route('/new')
def input_task():
    if current_user.is_authenticated:
        args = request.args
        type = args['type']
        if type == 'assignment':
            assignment = Task(name=args.get('name'), user_id=current_user.id, subject=args.get('subject'),
                              details=args.get('details'), due_time=args.get('due_time'),
                              percent_complete=args.get('percent_complete'), percent_worth=args.get('percent_worth'),
                              type="assignment")
            db.session.add(assignment)
            return jsonify({'status': 'success'})
        elif type == 'exam':
            exam = Task(name=args.get('name'), user_id=current_user.id, subject=args.get('subject'),
                        details=args.get('details'), due_time=args.get('due_time'),
                        percent_complete=args.get('percent_complete'), percent_worth=args.get('percent_worth'),
                        type="exam")
            db.session.add(exam)
        elif type == 'task':
            task = Task(name=args.get('name'), user_id=current_user.id, subject=args.get('subject'),
                        details=args.get('details'), due_time=args.get('due_time'),
                        percent_complete=args.get('percent_complete'), percent_worth=args.get('percent_worth'),
                        type="task")
            db.session.add(task)
    return jsonify({'status': 'failure'})


@app.route('/update')
def update_task():
    if current_user.is_authenticated:
        args = request.args

        task = Task.query.filter_by(id=args.get('id'), user_id=current_user.id).first()
        if task:
            task.percent_complete = args.get('value')
            db.session.commit()
            return jsonify({'status': 'success'})

        return jsonify({'status': 'failure'})


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


def calculate_work(tasks):
    for task in tasks:
        time_diff = task['due_time'] - int(datetime.utcnow().timestamp())

        score = 100 - task['percent_complete']
        score *= task['percent_worth']
        score *= 86400 / time_diff
        score *= 10000 / time_diff
        score *= 10

        task['score'] = score

        if time_diff <= 0:
            task['color'] = "white"
            task['score'] = 0
        elif score > 100:
            task['color'] = "red"
        elif score > 1:
            task['color'] = "yellow"
        else:
            task['color'] = "green"

    tasks = sorted(tasks, key=lambda k: k['score'], reverse=True)
    return tasks


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
    app.add_url_rule('/favicon.png', redirect_to=url_for('static', filename='favicon.png'))
