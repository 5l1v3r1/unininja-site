import os
from datetime import datetime
from urllib.parse import urlparse, urljoin

from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, logout_user, UserMixin

from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField, PasswordField
from wtforms.validators import DataRequired

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
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(255), unique=True)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    time = db.Column(db.Integer)

    def __repr__(self):
        return '<Task %r - %r>' % (self.id, self.name)


def create_user(name, email, password):
    if not User.query.filter_by(email=email).first():
        user = User(name=name, email=email, password=password, active=True, confirmed_at=datetime.utcnow())
        db.session.add(user)
        db.session.commit()
        return True
    else:
        return False


def check_user(email, password):
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        return user
    else:
        return None


@app.route('/')
def index():
    if current_user.is_authenticated:
        tab = request.args.get('tab') or 'home'
        return render_template('index.html', tab=tab)
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


@app.route('/work', methods=['GET', 'POST'])
def work():
    if session.get('time'):  # form submitted previously
        task, time_available = calculate_work()
        return render_template('work.html', task=task, time=time_available)

    form = TimeForm()
    if form.validate_on_submit():
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
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    app.add_url_rule('/favicon.png', redirect_to=url_for('static', filename='favicon.png'))
