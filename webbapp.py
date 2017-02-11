from flask import Flask, request, render_template
#from model import *
from flask import session as login_session
from flask import g

app = Flask(__name__)

#engine = create_engine('sqlite:///project.db')
#Base.metadata.bind = engine
#DBSession = sessionmaker(bind=engine)
#session = DBSession()

@app.route('/')
def main_page():
	#pics=session.query(Picture).filter_by(cover=True).all()
	return render_template('mainpage.html')

	
@app.route('/profile')
def showProfile():
	return render_template('profile.html')

@app.route('/aboutus')
def aboutus():
    return render_template("aboutus.html")

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template("login.html")

#@app.route('/logout', methods = ['POST'])
#def logout():
#	return "mainpage.html"

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
