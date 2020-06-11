from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm, UserForm, EditForm
from flask_mysqldb import MySQL
import yaml
app = Flask(__name__)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

app.config['SECRET_KEY'] = '34588d3cb014a1efde502716dacd3410'

posts = [   
    {
        'author': 'Muhamad Sechan Syadat',
        'title': 'Blog Post 1',
        'content': 'First Post Content',
        'date_posted': 'July 4, 2019',
    },
    {
        'author': 'Muhamad Ilham',
        'title': 'Blog Post 2',
        'content': 'Second Post Content',
        'date_posted': 'July 5, 2019',
    }
]

@app.route("/")
def index():
    return redirect(url_for('home'));
@app.route("/home")
def home():
    return render_template('home.html', posts=posts, title='Home')

@app.route("/about")
def about():
    return render_template('about.html', title='About')   

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'zxcvbnm':
            flash('You have been Logged in!','success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessfull. Please Check username & password', 'danger')
    return render_template('login.html', title='Login', form=form)    

@app.route("/users", methods=['GET', 'POST'])
def users():
    form=UserForm()
    if request.method == 'POST':
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email) VALUES(%s, %s)",(name, email))
        mysql.connection.commit()
        cur.close()
        # return 'success'
        if form.validate_on_submit():
            flash('Success', 'success')
            return redirect(url_for('users'))
    return render_template('users.html', title='Login', form=form)

@app.route('/data-users')
def datausers():
    cur=mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users")
    if resultValue > 0:
        userDetails = cur.fetchall()
        cur.close()
        return render_template('datauser.html',userDetails=userDetails)

@app.route('/edit/<int:id>')
def edit(id):
    form = EditForm()
    cur=mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users WHERE id=%s", id)
    if resultValue > 0:
        userDetails = cur.fetchone()
        cur.close()
        return render_template('edit.html', data=data)
    #     else:
    #         return 'Error loading #{id}'.format(id=id)
    # except Exception as e:
    #     print (e)
    # finally:
    #     cur.close()
    # return render_template('edit.html')

if __name__ == "__main__":
    app.run(debug=True)