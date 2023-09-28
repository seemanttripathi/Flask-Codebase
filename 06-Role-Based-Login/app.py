from flask import Flask, request, render_template, redirect, url_for
from flask_login import LoginManager, login_manager, login_user
from flask_security import Security, SQLAlchemySessionUserDatastore
from flask_security import UserMixin, RoleMixin
from flask_security import roles_accepted
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///g4g.sqlite3"
app.config['SECRET_KEY'] = 'MY_SECRET'
app.config['SECURITY_PASSWORD_SALT'] = "MY_SECRET"
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

roles_users = db.Table('roles_users',
		db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
		db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))
	
class User(db.Model, UserMixin):
	__tablename__ = 'user'
	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	email = db.Column(db.String, unique=True)
	password = db.Column(db.String(255), nullable=False, server_default='')
	active = db.Column(db.Boolean())
	roles = db.relationship('Role', secondary=roles_users, 
						 backref=db.backref('users', lazy='dynamic'))

class Role(db.Model, RoleMixin):
	__tablename__ = 'role'
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(80), unique=True)

@app.before_first_request
def create_tables():
	db.create_all()

user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
security = Security(app, user_datastore)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	msg=""
	if request.method == 'POST':
		user = User.query.filter_by(email=request.form['email']).first()
		if user:
			msg="User already exist"
			return render_template('signup.html', msg=msg)
		
		user = User(email=request.form['email'], active=1, password=request.form['password'])
		role = Role.query.filter_by(id=request.form['options']).first()
		user.roles.append(role)
		
		db.session.add(user)
		db.session.commit()
		
		login_user(user)
		return redirect(url_for('index'))
	else:
		return render_template("signup.html", msg=msg)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
	msg=""
	if request.method == 'POST':
		user = User.query.filter_by(email=request.form['email']).first()
		if user:
			if user.password == request.form['password']:
				login_user(user)
				return redirect(url_for('index'))
			else:
				msg="Wrong password"
		else:
			msg="User doesn't exist"
		return render_template('signin.html', msg=msg)
	else:
		return render_template("signin.html", msg=msg)

@app.route('/teachers')
@roles_accepted('Admin')
def teachers():
	teachers = []
	role_teachers = db.session.query(roles_users).filter_by(role_id=2)

	for teacher in role_teachers:
		user = User.query.filter_by(id=teacher.user_id).first()
		teachers.append(user)

	return render_template("teachers.html", teachers=teachers)

@app.route('/staff')
@roles_accepted('Admin', 'Teacher')
def staff():
	staff = []
	role_staff = db.session.query(roles_users).filter_by(role_id=3)
	for staf in role_staff:
		user = User.query.filter_by(id=staf.user_id).first()
		staff.append(user)
	return render_template("staff.html", staff=staff)

@app.route('/students')
@roles_accepted('Admin', 'Teacher', 'Staff')
def students():
	students = []
	role_students = db.session.query(roles_users).filter_by(role_id=4)
	for student in role_students:
		user = User.query.filter_by(id=student.user_id).first()
		students.append(user)
	return render_template("students.html", students=students)

@app.route('/mydetails')
@roles_accepted('Admin', 'Teacher', 'Staff', 'Student')
def mydetails():
	return render_template("mydetails.html")

if __name__ == "__main__":
	app.run(debug = True)
