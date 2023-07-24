from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {"apiKey": "AIzaSyC80DIkcnPCQXaArh3v8WvT68oIAKABQ1k",
  "authDomain": "zawardo-49c1e.firebaseapp.com",
  "projectId": "zawardo-49c1e",
  "storageBucket": "zawardo-49c1e.appspot.com",
  "messagingSenderId": "58476508356",
  "appId": "1:58476508356:web:5c2547be17d2a044ba4591", "databaseURL": "https://last-cs-lecture-default-rtdb.europe-west1.firebasedatabase.app/" }



firebase = pyrebase.initialize_app(config)
auth= firebase.auth()
db = firebase.database()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            print("HELLO, WORKED")
            return redirect(url_for('add_tweet'))
        except Exception as e:
            error = "Authentication failed"
            print(e)
    return render_template("signin.html")



@app.route('/signup', methods=['GET', 'POST'])
def signup(): 
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        bio = request.form['bio']
        full_name = request.form['fullname']
        
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {"name": full_name, "email": email, "username" : username, "bio" : bio}
            db.child("Users").child(UID).update(user)
            return redirect(url_for('add_tweet'))

        except:
            error = "Authentication failed"

    return render_template("signup.html")



@app.route('/signout')
def signout():
    auth.current_user = None
    login_session['user'] = None
    return redirect(url_for('signin'))

@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        try:
            UID = login_session['user']['localId']
            tweet = {'title':title, 'text':text, 'UID': UID}
            db.child("Tweets").push(tweet)
            return redirect(url_for('all_tweets'))
        except:
            error = "your dumb"
            

    return render_template("add_tweet.html")


@app.route('/all_tweets')
def all_tweets():
    
    UID = login_session['user']['localId']

    dici = db.child("Tweets").get().val()


    return render_template('tweet.html', tweet123 = dici)


if __name__ == '__main__':
    app.run(debug=True)