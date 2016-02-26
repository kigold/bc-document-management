from flask import Flask, render_template, request, redirect, url_for, session, g
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from sqlalchemy import create_engine

app = Flask(__name__)


############Database


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:blessed@localhost/postgres'
db = SQLAlchemy(app)

migrate = Migrate(app, db)
#manager.add_command('db', MigrateCommand)

#db.create_all()

'''Create Database model'''
class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	f_name = db.Column(db.String(120))
	s_name = db.Column(db.String(120))
	username = db.Column(db.String(120), unique=True)
	email = db.Column(db.String(120), unique=True)
	password = db.Column(db.String(120))
	position = db.Column(db.String(120))
	dept = db.Column(db.String(120))


	def __init__(self, username,f_name,s_name,email,password,position,dept):
		self.username = username
		self.f_name = f_name
		self.s_name = s_name
		self.email = email
		self.password = password
		self.position = position
		self.dept = dept

	def __repr__(self):
		return	'<username [{},{}]'.format(self.username, self.password)





class Documents(db.Model):
	__tablename__ = 'documents'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120), nullable=True)
	author = db.Column(db.String(120), nullable=True)
	link = db.Column(db.String(300), nullable=True)
	keyword = db.Column(db.String(300), nullable=True)
	dept = db.Column(db.String(120), nullable=True)


	def __init__(self, title):
		return '<title [{}, {}]'.format(self.title, self.id)

####



app.secret_key = "mykeyoogetit"
# login required decorator
def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			return redirect(url_for('login'))
	return wrap


#login required decorator


@app.route('/docs', )
@login_required
def docs():
	'''try:
		title = request.form['title']
		author = request.form['author']
		link = request.form['link']
		keyword = request.form['keyword']
		contributor = request.form['contributor']
	except "Server Error" as e:
			error = str(e)'''
	return render_template('documents.html')

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		user = User.query.filter_by(username=username).first()
		if str(user.password) == password:
			session['logged_in'] = True
			session['username'] = request.form['username']
			#flash('You have succesfuly loged in')
			return render_template('index.html')
		else:
			if request.form['username'] != 'admin' or request.form['password'] != 'admin':
				error = 'Invalid login credentials , Please try again.'
				return render_template('login.html', error=error)		
	return render_template('login.html')

@app.route('/logout') 
@login_required
def logout():
	session.pop('logged_in', None)
	#flash('You have logged out')
	return redirect(url_for('home'))

  
@app.route('/home')
@login_required
def home():
    return render_template('index.html') 


@app.route('/register', methods=['GET', 'POST'])
def reg():
	
	if request.method == 'POST':
		try:
			username = request.form['username']
			f_name = request.form['f_name']
			s_name = request.form['s_name']
			email = request.form['email']
			password = request.form['password']
			position = request.form['position']
			dept = request.form['dept']

			'''check is email doesnt already exist'''

			if not db.session.query(User).filter(User.email==
				email).count() and db.session.query(User).filter(User.password == password).count():
				client = User(username, f_name, s_name, password, email, position, dept)
				db.session.add(client)
				db.session.commit()

				'''set session anduser name '''

				session['logged_in'] = True
				session['username'] = request.form['username']

				#return render_template('user.html', name=username)
				return render_template('index.html')


			return render_template('user/' + str(username))
		except "Server Error" as e:
			error = str(e)
	return render_template('register.html')




@app.route('/user/<name>')
def user(name):
	return '<h1> Hello, %s!</h1>' % name


if __name__ == '__main__':
    app.run(debug=True)


