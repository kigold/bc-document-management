from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from sqlalchemy import create_engine


app = Flask(__name__)


# Database

app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:blessed@localhost/postgres'
db = SQLAlchemy(app)

# migrate = Migrate(app, db)
# manager.add_command('db', MigrateCommand)




'''Create Database model'''


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(120))
    s_name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    position = db.Column(db.String(120))
    dept = db.Column(db.String(120))

    def __init__(self, f_name, s_name, email, password, position, dept):
        self.f_name = f_name
        self.s_name = s_name
        self.email = email
        self.password = password
        self.position = position
        self.dept = dept

    def __repr__(self):
        return '<username [{},{}]'.format(self.f_name, self.password)


class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=True, index=True)
    author = db.Column(db.String(120), nullable=True)
    link = db.Column(db.String(300), nullable=True)
    keyword = db.Column(db.String(300), nullable=True)
    contributor = db.Column(db.String(300), nullable=True)
    dept = db.Column(db.String(120), nullable=True)


    def __init__(self, title, author, link, keyword, contributor, dept):
        self.title = title
        self.author = author
        self.link = link
        self.keyword = keyword
        self.contributor = contributor
        self.dept = dept

    def __repr__(self):
        return '<title [{}, {}]'.format(self.title, self.id)


db.create_all()

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


# login required decorator


@app.route('/docs', methods=['GET', 'POST'])
@login_required
def docs():
    ''' variable to be passed to page'''

    color = {0 : 'success', 1 : 'danger', 2 : 'info'}
    all_docs = Document.query.all()
    count = 1
    if request.method == 'POST':
        try:
            '''  create dictionary for color alternation of table'''
            title = request.form['title']
            author = session['id'] #User.query.filter_by(id=session['id']).first().f_name
            link = request.form['link']
            keyword = request.form['keyword']
            contributor = request.form['contributor']
            dept = request.form['dept']
            doc = Document(title, author, link, keyword, contributor, dept)
            if not Document.query.filter_by(title=title).count():
                db.session.add(doc)
                db.session.commit()
                flash(title + " successfully updated")
            else:
                flash(
                    "One documents with the title " + title + " already exists \n ")
                doc = Document.query.filter_by(title=title).first()
                flash('Title: %r Author: %r Link: %r Keyword: %r \
                    Contributor: %r Dept%r >' % (str(doc.title), \
                        str(doc.author), str(doc.link), str(doc.keyword), str(doc.contributor), str(doc.dept)))
            return render_template('documents.html', color=color, docs=all_docs, count=count)
        except "Server Error" as e:
            error = str(e)
    

    return render_template('documents.html', color=color, docs=all_docs, count=count)


@app.route('/')
#@login_required
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        password = request.form['password']
        email = request.form['username']
        user = User.query.filter_by(email=email).first()
        if user is not None and str(user.password) == password:
            session['logged_in'] = True
            session['username'] = user.f_name
            session['id'] = user.id
            flash('You are logged in')
            return render_template('index.html')
        else:
            error = 'Invalid login credentials , Please try again.'
            flash("Invalid login credential")
            return render_template('login.html', error=error)
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    # flash('You have logged out')
    return redirect(url_for('home'))


@app.route('/home')
#@login_required
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def reg():

    if request.method == 'POST':
        try:
            f_name = request.form['f_name']
            s_name = request.form['s_name']
            email = request.form['email']
            password = request.form['password']
            position = request.form['position']
            dept = request.form['dept']

            '''check is email doesnt already exist'''
            
            if not User.query.filter_by(email=email).count():
                client = User(f_name, s_name, email, password, position, dept)
                db.session.add(client)
                db.session.commit()
                flash('You have successfully registered ' + email + "\n\
                      , pls login")
                return redirect(url_for('login'))
            return render_template('index.html')
        except "Server Error" as e:
            error = str(e)
    return render_template('register.html')


@app.route('/admin')
def admin():

    users = User.query.all()
    result = ""
    for user in users:
        result += str(user) + "\n"
    return '<h1> Hello, %s!</h1>' % result


@app.route('/user/<name>')
def user(name):
    users = User.query.all()
    result = ""
    for user in users:
        result += str(user) + "\n"
    return '<h1> Hello, %s!</h1>' % name


if __name__ == '__main__':
    app.run(debug=True)
