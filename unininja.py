from flask import *
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
with open('db_uri', 'r') as f:
    f = f.read()
    app.config['SQLALCHEMY_DATABASE_URI'] = f
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class TimeForm(FlaskForm):
    time = StringField('Seconds', validators=[DataRequired()])
    submit = SubmitField('Submit')


class TasksForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    length = StringField('Length', validators=[DataRequired()])
    submit = SubmitField('Submit')


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


@app.route('/work', methods=['GET', 'POST'])
def work():
    if session.get('time'):  # form submitted previously
        task, time_available = calculate_work()
        return render_template('work.html', task=task, time=time_available)

    form = TimeForm()
    if form.validate_on_submit():  # No form submitted
        session['time'] = form.time.data
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
    app.config['SECRET_KEY'] = 'just a test string for now, change later'
    app.run(debug=True)
