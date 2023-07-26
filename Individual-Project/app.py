from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config={
  "apiKey": "AIzaSyCKYIjf92qJr8xux2xGyb58JunfNMzZXy0",
  "authDomain": "elena-94419.firebaseapp.com",
  "projectId": "elena-94419",
  "storageBucket": "elena-94419.appspot.com",
  "messagingSenderId": "554917943404",
  "appId": "1:554917943404:web:24a1b0cbab82ee79ada049",
  'measurementId': "G-QNFK0V3H22",
  "databaseURL": "https://elena-94419-default-rtdb.firebaseio.com"
  }
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database ()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


users = []


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('survey'))
        except:
            error = "Authentication failed"
    return render_template('login.html')

@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']

        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {'email': email, 'username': username}
            db.child("Users").child(UID).set(user)
            return redirect(url_for('survey'))

        except:
            error = "Authentication failed"
    return render_template('signup.html')

@app.route('/survey')
def survey():
    UID = login_session['user']['localId']
    user = db.child("Users").child(UID).get().val()
    return render_template('survey.html', user = user['username'])

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'GET':
        return render_template('login.html')

@app.route('/happy', methods=['GET', 'POST'])
def happy():
    if request.method == 'GET':
        return render_template('happy.html')





#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)