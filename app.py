from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps

app = Flask(__name__)

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

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] == 'admin' and request.form['password'] == 'admin':
			username = request.form['username']
			session['logged_in'] = True
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
	error = None
	if request.method == 'POST':
		try:
			username = request.form['username']
			return render_template('user/' + str(username))
		except "Server Error" as e:
			error = str(e)
	return render_template('register.html')





@app.route('/user/<name>')
def user(name):
	return '<h1> Hello, %s!</h1>' % name


if __name__ == '__main__':
    app.run(debug=True)


