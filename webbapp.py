from flask import Flask, request, url_for, render_template, redirect
from model import *
from flask import session as login_session
from flask import g

app = Flask(__name__)
app.secret_key = "MYSECRETKEY"
engine = create_engine('sqlite:///quotes.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def main_page():
	#pics=session.query(Picture).filter_by(cover=True).all()
	return render_template('mainpage.html')

	
@app.route('/login')
def logmein():
	return render_template('login.html')

@app.route('/aboutus')
def aboutus():
    return render_template("aboutus.html")

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if verify_password(email, password):
            user = session.query(User).filter_by(email=email).first()
            login_session['name'] = user.name
            login_session['id'] = user.id
            login_session['email'] = user.email
            return redirect(url_for('main_page'))
@app.route("/logout")
def logout():
    del login_session['id']
    del login_session['name']
    del login_session['email']
    return redirect(url_for('main_page'))

def verify_password(email, password):
    user = session.query(User).filter_by(email=email).first()
    if not user or not user.verify_password(password):
        return False
    return True


@app.route('/signup', methods = ['GET','POST'])
def signup():
    if request.method == 'POST':
    	
        name = request.form['username'] 
        password = request.form['password']
        
        if name is None or password is None:
            flash("Your form is missing arguments")
            return redirect(url_for('newCustomer'))
        if session.query(Customer).filter_by(email = email).first() is not None:
            flash("A user with this email address already exists")
            return redirect(url_for('newCustomer'))
        customer = Customer(name = name, email=email, address = address)
        customer.hash_password(password)
        session.add(customer)
        shoppingCart = ShoppingCart(customer=customer)
        session.add(shoppingCart)
        session.commit()
        flash("User Created Successfully!")
        return redirect(url_for('inventory'))
    else:
        return render_template('signup.html')

if __name__ == '__main__':
	app.run(debug=True)
