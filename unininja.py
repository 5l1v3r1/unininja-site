from flask import *
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import datetime

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)

roles_users = db.Table('roles_users', db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class TimeForm(FlaskForm):
    working_time = HiddenField('Seconds', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class SignupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    time = db.Column(db.Integer)

    def __repr__(self):
        return '<Task %r - %r>' % (self.id, self.name)


def create_user(name, email, password):
    db.create_all()

    db.create_user(name=name, email=email, password=password)
    db.session.commit()


@app.route('/')
def index():
    tab = request.args.get('tab') or 'home'
    return render_template('index.html', tab=tab)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        create_user(form.name. form.email, form.password)
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)


@app.route('/signin')
def signin():
    return render_template('signup.html')


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
    session.clear()
    return redirect(url_for('index'))


def calculate_work():
    return Task.query.first(), session.get('time')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
