import random
from flask import Flask, render_template, request, make_response, redirect, url_for
from models import User, db
import uuid
import hashlib

app = Flask(__name__)
db.create_all()

MAX_SECRET = 30


def get_user(user_token=None):
    if not user_token:
        user_token = request.cookies.get('token')
    return db.query(User).filter_by(session_token=user_token).first()


@app.route('/', methods=['GET'])
def index():
    user = get_user()
    return render_template('index.html', user=user, max_secret=MAX_SECRET)


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        response = render_template('login.html')
    else:
        name = request.form.get('user-name')
        email = request.form.get('user-email')
        password = str(request.form.get('user-pass'))
        password = hashlib.sha256(password.encode()).hexdigest()

        user = db.query(User).filter_by(email=email).first()
        if not user:
            secret = random.randint(1, MAX_SECRET)
            user = User(name=name, email=email, secret_number=secret, passwd=password)
            db.add(user)
            db.commit()

        if password != user.passwd:
            return "Napačno geslo!!!!"

        token = str(uuid.uuid4())
        user.session_token = token
        db.add(user)
        db.commit()

        response = make_response(redirect(url_for('index')))
        response.set_cookie('token', token, httponly=True, samesite='strict')

    return response


@app.route("/result", methods=["POST"])
def result():
    guess = int(request.form.get("guess"))
    user = get_user()
    if not user:
        return redirect(url_for('login'))

    if guess == user.secret_number:
        message = "Pravilno! Skrito število je {0}".format(str(user.secret_number))
        response = make_response(render_template("result.html", finished=True, message=message))
        user.secret_number = random.randint(1, MAX_SECRET)
        db.add(user)
        db.commit()
        return response
    elif guess > user.secret_number:
        message = "Ta poizkus ni pravilen. Poizkusi z manjšo številko."
        return render_template("result.html", finished=False, message=message)
    elif guess < user.secret_number:
        message = "Ta poizkus ni pravilen. Poizkusi z večjo številko."
        return render_template("result.html", finished=False,  message=message)


if __name__ == '__main__':
    app.run()
